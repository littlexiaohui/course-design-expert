#!/usr/bin/env python3
"""Check inline Markdown links to relative files, without network access."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    checked = 0
    missing = []
    for markdown in ROOT.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        content = markdown.read_text(encoding="utf-8")
        for match in LINK.finditer(content):
            target = match.group(1).strip().strip("<>")
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            path = Path(unquote(parts.path))
            checked += 1
            resolved = (markdown.parent / path).resolve()
            if path.is_absolute() or not resolved.is_relative_to(ROOT) or not resolved.exists():
                line = content.count("\n", 0, match.start()) + 1
                missing.append(f"{markdown.relative_to(ROOT)}:{line}: {target}")
    for item in missing:
        print(f"Invalid relative link: {item}", file=sys.stderr)
    print(f"Checked {checked} relative file links; invalid: {len(missing)}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
