#!/usr/bin/env python3
"""Copy reviewed Skill files to the repository root; never commit or push."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent


def relative_path(value: str) -> Path:
    p = PurePosixPath(value)
    if not value or p.is_absolute() or any(part in {".", ".."} for part in p.parts):
        raise ValueError(f"Unsafe manifest path: {value!r}")
    return Path(*p.parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Authoritative Skill directory")
    parser.add_argument("--check", action="store_true", help="Compare only; write nothing")
    args = parser.parse_args()
    config = json.loads((ROOT / "sync-manifest.json").read_text(encoding="utf-8"))
    if config.get("version") != 1 or config.get("skill") != "course-design-expert":
        raise ValueError("Unsupported sync manifest")
    files = [relative_path(x) for x in config["files"]]
    excluded = {relative_path(x) for x in config["excluded"]}
    if len(set(files)) != len(files) or set(files) & excluded:
        raise ValueError("Manifest has duplicate or conflicting entries")

    source = args.source.resolve(strict=True)
    if not source.is_dir():
        raise ValueError("Source must be a directory")
    actual = {p.relative_to(source) for p in source.rglob("*")
              if p.is_file() and p.name != ".DS_Store" and "__pycache__" not in p.parts}
    unknown = sorted(actual - set(files) - excluded)
    missing = sorted(set(files) - actual)
    if unknown or missing:
        for p in unknown:
            print(f"Unreviewed source file: {p}", file=sys.stderr)
        for p in missing:
            print(f"Missing required source file: {p}", file=sys.stderr)
        return 2

    references = ROOT / "references"
    present = {p.relative_to(ROOT) for p in references.rglob("*") if p.is_file()} if references.exists() else set()
    extra = present - set(files)
    if extra:
        for p in sorted(extra):
            print(f"Unexpected distribution reference: {p}", file=sys.stderr)
        return 2

    contents = {}
    for rel in files:
        src = source / rel
        dst = ROOT / rel
        if src.is_symlink() or not src.resolve().is_relative_to(source):
            raise ValueError(f"Source symlink escapes or is not allowed: {rel}")
        if dst.is_symlink() or not dst.resolve().is_relative_to(ROOT):
            raise ValueError(f"Unsafe distribution path: {rel}")
        contents[rel] = src.read_bytes()
    changed = [rel for rel, data in contents.items()
               if not (ROOT / rel).is_file() or (ROOT / rel).read_bytes() != data]
    if args.check:
        for rel in changed:
            print(f"Different: {rel}")
        print(f"Checked {len(files)} files; differences: {len(changed)}")
        return 1 if changed else 0

    if (ROOT / ".git").exists():
        status = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all",
                                 "--", "SKILL.md", "references"], capture_output=True, text=True, check=True)
        if status.stdout.strip():
            print("Distribution Skill has uncommitted changes; review them before syncing.", file=sys.stderr)
            return 2
    for rel in changed:
        dst = ROOT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(contents[rel])
    print(f"Synced {len(changed)} of {len(files)} reviewed files; no commit or push was made.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"Sync failed: {exc}", file=sys.stderr)
        raise SystemExit(2)
