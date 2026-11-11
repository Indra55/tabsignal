#!/usr/bin/env python3
"""Build a clean Chrome Web Store upload ZIP from the extension runtime files."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import json

ROOT = Path(__file__).resolve().parents[1]
STORE = Path(__file__).resolve().parent


def main():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    version = manifest["version"]
    files = [
        "manifest.json",
        "content.js",
        "popup.html",
        "popup.css",
        "popup.js",
        "icons/chatgpt.svg",
        "icons/deepseek.svg",
        "icons/gemini.png",
        "icons/grok.svg",
        "icons/icon-16.png",
        "icons/icon-32.png",
        "icons/icon-128.png",
        "icons/tabsignal.svg",
    ]
    target = STORE / "package" / f"TabSignal-{version}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in files:
            source = ROOT / relative
            if not source.is_file():
                raise FileNotFoundError(source)
            archive.write(source, arcname=relative)
    print(f"Created {target} ({len(files)} files)")


if __name__ == "__main__":
    main()
