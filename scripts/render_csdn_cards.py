#!/usr/bin/env python3
"""Render both README card themes from the cached CSDN total views."""

import json
from pathlib import Path
import re


def render_cards(stats_path: Path, output_dir: Path) -> None:
    raw_views = json.loads(stats_path.read_text(encoding="utf-8"))["views"]
    if not isinstance(raw_views, (str, int)) or isinstance(raw_views, bool):
        raise ValueError("CSDN views must be a non-negative integer")
    raw_views = str(raw_views).strip()
    if not re.fullmatch(r"[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+", raw_views):
        raise ValueError("Invalid CSDN views value")
    views = f"{int(raw_views.replace(',', '')):,}"

    palettes = {
        "light": ("#fbfcfd", "#dde3e8", "#222c37", "#36877b"),
        "dark": ("#151b23", "#303a45", "#edf2f7", "#83c8bb"),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for theme, (background, border, foreground, accent) in palettes.items():
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="104" viewBox="0 0 400 104" role="img" aria-label="CSDN: {views} views">
  <title>CSDN: {views} views</title>
  <rect x="1" y="1" width="398" height="94" rx="14" fill="{background}" stroke="{border}" stroke-width="2"/>
  <g transform="translate(27 32)" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 8H7a4 4 0 0 0-4 4v8a4 4 0 0 0 4 4h4m10-16h4a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4h-4M18 5l-4 22"/></g>
  <g font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif">
    <text x="84" y="38" fill="{foreground}" font-size="28" font-weight="600">CSDN</text>
    <text x="84" y="69" fill="{accent}" font-size="23" font-weight="500">{views} views</text>
  </g>
</svg>
'''
        (output_dir / f"csdn-{theme}.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    render_cards(root / "data/csdn-stats.json", root / "assets/links")
