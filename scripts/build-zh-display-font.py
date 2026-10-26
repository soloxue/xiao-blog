"""Subset the Chinese display font for the site's current headings.

Usage: python scripts/build-zh-display-font.py --source PATH_TO_ZHUQUE_TTF
The source font is not redistributed; its OFL notice is kept in fonts/.
"""

from __future__ import annotations

import argparse
import subprocess
from html.parser import HTMLParser
from pathlib import Path

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "fonts" / "zhuque-display.woff2"


class Headings(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in self.stack:
            self.stack = self.stack[: len(self.stack) - 1 - self.stack[::-1].index(tag)]

    def handle_data(self, data: str) -> None:
        if any(tag in self.stack for tag in ("nav", "h1", "h2", "h3")):
            self.text.append(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()

    source = args.source.resolve(strict=True)
    headings = Headings()
    pages = sorted(ROOT.glob("**/cn.html")) + sorted(ROOT.glob("**/index.cn.html"))
    for page in pages:
        headings.feed(page.read_text(encoding="utf-8"))
        headings.reset()

    chars = set("".join(headings.text))
    chars.update("朱雀仿宋")
    chars.discard("❦")  # Decorative mark retains its existing fallback face.
    available = TTFont(source, lazy=True).getBestCmap()
    missing = sorted(char for char in chars if not char.isspace() and ord(char) not in available)
    if missing:
        raise SystemExit(f"Source font lacks heading glyphs: {''.join(missing)}")

    subprocess.run(
        [
            "pyftsubset",
            str(source),
            f"--text={''.join(sorted(chars))}",
            "--flavor=woff2",
            f"--output-file={OUTPUT}",
        ],
        check=True,
    )
    included = TTFont(OUTPUT, lazy=True).getBestCmap()
    omitted = sorted(char for char in chars if not char.isspace() and ord(char) not in included)
    if omitted:
        raise SystemExit(f"Subset lacks heading glyphs: {''.join(omitted)}")
    print(f"{len(pages)} Chinese pages; {len(chars)} heading characters; {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
