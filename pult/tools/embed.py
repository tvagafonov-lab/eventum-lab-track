#!/usr/bin/env python3
"""Вшивает pult/product.yaml в pult/panel.html между маркерами PULT:DATA."""
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP = ROOT / "product.yaml"
PANEL = ROOT / "panel.html"
START = "<!-- PULT:DATA:START -->"
END = "<!-- PULT:DATA:END -->"


def main() -> int:
    data = yaml.safe_load(MAP.read_text(encoding="utf-8"))
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # </script> внутри JSON-строк не должен разрывать тег
    payload = payload.replace("</", "<\\/")
    block = (
        f"{START}\n"
        f'<script type="application/json" id="pult-data">{payload}</script>\n'
        f"{END}"
    )
    html = PANEL.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(html):
        sys.exit("panel.html: маркеры PULT:DATA не найдены")
    PANEL.write_text(pattern.sub(lambda _: block, html), encoding="utf-8")
    print(f"ok: {MAP.name} → {PANEL.name} ({len(payload)} байт данных)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
