#!/usr/bin/env python3
"""Manage manifests/source-digests.json entries."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


MANIFEST = Path("manifests") / "source-digests.json"
SKIP_DIRS = {".git", "__pycache__"}


def normalize(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def resolve_repo_path(root: Path, raw_path: str) -> Path:
    normalized = normalize(raw_path)
    candidate = Path(normalized)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise SystemExit("Path must stay inside the repository.")
    resolved = (root / candidate).resolve()
    resolved.relative_to(root.resolve())
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_tree_files(path: Path) -> list[Path]:
    files: list[Path] = []
    for child in path.rglob("*"):
        if not child.is_file():
            continue
        if any(part in SKIP_DIRS for part in child.relative_to(path).parts):
            continue
        files.append(child)
    return sorted(files)


def sha256_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for child in iter_tree_files(path):
        digest.update(child.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(child).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def load_manifest(root: Path) -> dict:
    path = root / MANIFEST
    if not path.exists():
        return {
            "version": 1,
            "description": "Optional sha256 manifest for source files that have been reviewed into wiki summaries.",
            "entries": [],
        }
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise SystemExit("Unsupported source-digests.json format.")
    data.setdefault("entries", [])
    if not isinstance(data["entries"], list):
        raise SystemExit("source-digests.json entries must be a list.")
    return data


def save_manifest(root: Path, data: dict) -> None:
    path = root / MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    data["entries"] = sorted(data.get("entries", []), key=lambda item: item["path"])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def entry_for(root: Path, raw_path: str, kind: str | None) -> dict:
    normalized = normalize(raw_path)
    source = resolve_repo_path(root, normalized)
    if not source.exists():
        raise SystemExit(f"Source not found: {normalized}")
    actual_kind = kind or ("tree" if source.is_dir() else "file")
    if actual_kind == "file" and not source.is_file():
        raise SystemExit(f"Expected file: {normalized}")
    if actual_kind == "tree" and not source.is_dir():
        raise SystemExit(f"Expected directory: {normalized}")
    digest = sha256_file(source) if actual_kind == "file" else sha256_tree(source)
    return {"path": normalized, "kind": actual_kind, "sha256": digest}


def find_entry(data: dict, path: str) -> dict | None:
    normalized = normalize(path)
    for entry in data.get("entries", []):
        if entry.get("path") == normalized:
            return entry
    return None


def cmd_list(root: Path, _args: argparse.Namespace) -> int:
    data = load_manifest(root)
    entries = data.get("entries", [])
    if not entries:
        print("source_digest: no entries")
        return 0
    for entry in entries:
        print(f"{entry.get('kind', 'file')}\t{entry.get('sha256')}\t{entry.get('path')}")
    return 0


def cmd_add(root: Path, args: argparse.Namespace) -> int:
    data = load_manifest(root)
    normalized = normalize(args.path)
    existing = find_entry(data, normalized)
    if existing and not args.force:
        raise SystemExit(f"Entry already exists: {normalized}. Use update or --force.")
    new_entry = entry_for(root, normalized, args.kind)
    if existing:
        existing.update(new_entry)
    else:
        data["entries"].append(new_entry)
    save_manifest(root, data)
    print(f"source_digest: added {new_entry['path']} ({new_entry['kind']})")
    return 0


def cmd_update(root: Path, args: argparse.Namespace) -> int:
    data = load_manifest(root)
    normalized = normalize(args.path)
    existing = find_entry(data, normalized)
    if not existing:
        raise SystemExit(f"Entry not found: {normalized}. Use add first.")
    new_entry = entry_for(root, normalized, args.kind or existing.get("kind"))
    existing.update(new_entry)
    save_manifest(root, data)
    print(f"source_digest: updated {new_entry['path']} ({new_entry['kind']})")
    return 0


def cmd_remove(root: Path, args: argparse.Namespace) -> int:
    data = load_manifest(root)
    normalized = normalize(args.path)
    before = len(data.get("entries", []))
    data["entries"] = [entry for entry in data.get("entries", []) if entry.get("path") != normalized]
    if len(data["entries"]) == before:
        raise SystemExit(f"Entry not found: {normalized}")
    save_manifest(root, data)
    print(f"source_digest: removed {normalized}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List digest entries.").set_defaults(func=cmd_list)

    add = sub.add_parser("add", help="Add a source digest entry.")
    add.add_argument("path")
    add.add_argument("--kind", choices=("file", "tree"))
    add.add_argument("--force", action="store_true", help="Overwrite an existing entry.")
    add.set_defaults(func=cmd_add)

    update = sub.add_parser("update", help="Update an existing source digest entry.")
    update.add_argument("path")
    update.add_argument("--kind", choices=("file", "tree"))
    update.set_defaults(func=cmd_update)

    remove = sub.add_parser("remove", help="Remove a source digest entry.")
    remove.add_argument("path")
    remove.set_defaults(func=cmd_remove)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    return args.func(root, args)


if __name__ == "__main__":
    raise SystemExit(main())
