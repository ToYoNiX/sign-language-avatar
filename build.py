#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
WEB_DIR = ROOT / "web-simulator"
TEMPLATES_DIR = ROOT / "templates"
OUT_DIR = ROOT / "pages"


def build(origin: str) -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)

    shutil.copytree(WEB_DIR, OUT_DIR, symlinks=False)

    avatar_html = (TEMPLATES_DIR / "avatar.html").read_text(encoding="utf-8")
    avatar_html = avatar_html.replace("__ALLOWED_ORIGIN__", origin)
    (OUT_DIR / "avatar.html").write_text(avatar_html, encoding="utf-8")

    shutil.copy2(TEMPLATES_DIR / "playground.html", OUT_DIR / "playground.html")

    print(f"Built to {OUT_DIR}/ with origin={origin!r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build static site for GitHub Pages")
    parser.add_argument("--origin", default="*", help="Allowed origin for postMessage (default: *)")
    args = parser.parse_args()
    build(args.origin)
