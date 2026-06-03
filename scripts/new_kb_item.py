#!/usr/bin/env python3
"""Create small knowledge-base items from repository templates."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


CYRILLIC = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu",
    "я": "ya",
}


def slugify(value: str) -> str:
    transliterated = "".join(CYRILLIC.get(char.lower(), char.lower()) for char in value)
    slug = re.sub(r"[^a-z0-9]+", "-", transliterated).strip("-")
    return slug or "item"


def today() -> str:
    return dt.date.today().isoformat()


def write_file(path: Path, text: str, force: bool, dry_run: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    if dry_run:
        print(f"DRY-RUN write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"created {path}")


def source_note(title: str, scope: str, date: str) -> tuple[Path, str]:
    if scope not in {"personal", "work"}:
        raise SystemExit("source-note requires --scope personal or --scope work.")
    slug = slugify(title)
    path = Path("raw") / scope / "inbox" / f"{date}-{slug}.md"
    text = f"""# {date} {title}

Source type:
Privacy: Personal | Work | Sensitive | Public
Created: {date}

## Raw Notes

-

## Facts

-

## Inferences

-

## Hypotheses

-

## Open Questions

-

## Follow-up

-
"""
    return path, text


def concept(title: str, scope: str, date: str) -> tuple[Path, str]:
    slug = slugify(title)
    path = Path("wiki") / "concepts" / f"{slug}.md"
    text = f"""---
type: concept
scope: {scope}
status: draft
updated: {date}
sources: []
---

# {title}

## Summary

## Facts

## Inferences

## Open Questions

## Sources

## Related
"""
    return path, text


def project(title: str, scope: str, date: str) -> tuple[Path, str]:
    slug = slugify(title)
    path = Path("wiki") / "projects" / f"{slug}.md"
    text = f"""---
type: project
scope: {scope}
status: draft
updated: {date}
sources: []
---

# {title}

## Summary

## Current Status

## Key Decisions

## Source Material

## Next Actions

## Open Questions
"""
    return path, text


def decision(title: str, scope: str, date: str) -> tuple[Path, str]:
    slug = slugify(title)
    path = Path("wiki") / "decisions" / f"{date}-{slug}.md"
    text = f"""# {date} {title}

Status: proposed
Date: {date}
Scope: {scope}
Owner: repository owner

## Context

## Decision

## Alternatives Considered

## Consequences

## Sources

## Follow-up
"""
    return path, text


def asset_note(title: str, _scope: str, date: str) -> tuple[Path, str]:
    slug = slugify(title)
    path = Path("raw") / "assets" / f"{date}-{slug}.md"
    text = f"""# {date} Asset - {title}

Asset path:
Privacy: Public | Personal | Work | Sensitive
Created: {date}

## Summary

## Related Context

## Sources
"""
    return path, text


def meeting(title: str, scope: str, date: str) -> list[tuple[Path, str]]:
    if scope not in {"personal", "work"}:
        raise SystemExit("meeting requires --scope personal or --scope work.")
    slug = slugify(title)
    base = Path("raw") / scope / "meetings" / date[:4] / f"{date}-{slug}"
    summary = f"""---
type: meeting-summary
scope: {scope}
date: {date}
title: {title}
source_transcript:
participants: []
related_projects: []
updated: {date}
---

# {date} - {title}

## Source

- Transcript:
- Recording:

## Summary

## Facts

## Decisions

## Action Items

| Action | Owner | Due | Source |
|---|---|---|---|

## Open Questions

## Links
"""
    source = f"""# Source - {date} {title}

Origin:
Captured by:
Privacy: Personal | Work | Sensitive

## Files

- transcript.txt:
- recording:
- attachments:
"""
    return [(base / "summary.md", summary), (base / "source.md", source)]


BUILDERS = {
    "source-note": lambda title, scope, date: [source_note(title, scope, date)],
    "concept": lambda title, scope, date: [concept(title, scope, date)],
    "project": lambda title, scope, date: [project(title, scope, date)],
    "decision": lambda title, scope, date: [decision(title, scope, date)],
    "asset-note": lambda title, scope, date: [asset_note(title, scope, date)],
    "meeting": meeting,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=sorted(BUILDERS))
    parser.add_argument("title", help="Human-readable title.")
    parser.add_argument("--scope", default="personal", choices=("personal", "work", "mixed", "repo"))
    parser.add_argument("--date", default=today())
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    parser.add_argument("--dry-run", action="store_true", help="Print paths without writing files.")
    args = parser.parse_args(argv)

    for path, text in BUILDERS[args.kind](args.title, args.scope, args.date):
        write_file(path, text, args.force, args.dry_run)
    print("next: review the file, add source content, then run scripts/wiki_lint.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
