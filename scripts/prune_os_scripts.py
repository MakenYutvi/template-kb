#!/usr/bin/env python3
"""Remove script wrappers for operating systems not used by this checkout."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


WINDOWS_EXTENSIONS = {".bat", ".cmd", ".ps1"}
UNIX_EXTENSIONS = {".sh"}


@dataclass(frozen=True)
class Candidate:
    path: str
    reason: str


def detect_target() -> str:
    return "windows" if sys.platform.startswith("win") else "unix"


def resolve_root(raw_root: str) -> Path:
    root = Path(raw_root).resolve()
    if not root.exists():
        raise SystemExit(f"Repository root does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"Repository root is not a directory: {root}")
    return root


def removable_extensions(target: str) -> set[str]:
    if target == "windows":
        return UNIX_EXTENSIONS
    if target == "unix":
        return WINDOWS_EXTENSIONS
    raise ValueError(f"Unsupported target: {target}")


def list_candidates(root: Path, target: str) -> list[Candidate]:
    scripts_dir = root / "scripts"
    if not scripts_dir.exists():
        return []

    extensions = removable_extensions(target)
    candidates: list[Candidate] = []
    for path in sorted(scripts_dir.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix not in extensions:
            continue
        rel_path = path.relative_to(root).as_posix()
        candidates.append(
            Candidate(
                path=rel_path,
                reason=f"not used by target OS '{target}'",
            )
        )
    return candidates


def remove_candidates(root: Path, candidates: list[Candidate]) -> None:
    for candidate in candidates:
        path = (root / candidate.path).resolve()
        path.relative_to(root)
        path.unlink()


def print_text(candidates: list[Candidate], target: str, applied: bool) -> None:
    action = "deleted" if applied else "would delete"
    if not candidates:
        print(f"prune_os_scripts: no non-{target} script wrappers found.")
        return

    for candidate in candidates:
        print(f"{action}: {candidate.path} ({candidate.reason})")
    if not applied:
        print("dry-run only; rerun with --apply to delete these files.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument(
        "--target",
        choices=("auto", "windows", "unix"),
        default="auto",
        help="Target operating system. Defaults to auto-detecting the current OS.",
    )
    parser.add_argument("--apply", action="store_true", help="Delete files. Without this, only print a dry-run plan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = parser.parse_args(argv)

    root = resolve_root(args.root)
    target = detect_target() if args.target == "auto" else args.target
    candidates = list_candidates(root, target)

    if args.apply:
        remove_candidates(root, candidates)

    if args.json:
        print(
            json.dumps(
                {
                    "target": target,
                    "applied": args.apply,
                    "candidates": [asdict(candidate) for candidate in candidates],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print_text(candidates, target, args.apply)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
