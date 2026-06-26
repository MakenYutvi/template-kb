#!/usr/bin/env python3
"""Lightweight lint checks for a personal knowledge base repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote


MARKDOWN_ROOTS = (
    "AGENTS.md",
    "CLAUDE.md",
    "CHANGELOG.md",
    "README.md",
    "SETUP.md",
    ".ai",
    "wiki",
    "indexes",
    "manifests",
    "prompts",
    "docs",
    "raw",
)

TEXT_ROOTS = MARKDOWN_ROOTS + (
    ".gitignore",
    "requirements.txt",
    "scripts",
)

BINARY_EXTENSIONS = {
    ".docx",
    ".gif",
    ".jpeg",
    ".jpg",
    ".mov",
    ".mp4",
    ".pdf",
    ".png",
    ".pptx",
    ".webp",
    ".xlsx",
}

REQUIRED_MANIFEST_PATHS = (
    "raw/personal/",
    "raw/personal/meetings/",
    "raw/work/",
    "raw/work/meetings/",
    "raw/assets/",
    "wiki/",
    "wiki/outputs/",
    "wiki/health/",
    "wiki/people/",
    "indexes/",
    "prompts/",
    "scripts/",
)

SOURCE_DIGEST_MANIFEST = Path("manifests") / "source-digests.json"

LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
LOG_HEADING_RE = re.compile(r"^## \d{4}-\d{2}-\d{2} \| [a-z-]+ \| [a-z0-9-]+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
OUTPUT_FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*\.md$")
HEALTH_FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-health(?:-[a-z0-9][a-z0-9-]*)?\.md$")
LEGACY_WORK_PATH = "work" + "/"
LEGACY_PERSONAL_PATH = "personal" + "/"
OLD_CYCLE = "source -> " + "ingest"
OLD_DEPTH_EXPR = "parents" + "[4]"
OLD_ROOT_PATH_RE = re.compile(
    rf"(^|[^A-Za-z0-9_/]){re.escape(LEGACY_WORK_PATH)}"
    rf"|(^|[^A-Za-z0-9_/]){re.escape(LEGACY_PERSONAL_PATH)}"
)

DEFAULT_WIKI_PAGE_SOFT_LIMIT = 220
DEFAULT_WIKI_PAGE_HARD_LIMIT = 350
PAGE_BUDGETS = (
    ("wiki/log.md", 400, 800),
    ("wiki/decisions/", 120, 220),
    ("wiki/outputs/", 300, 600),
    ("wiki/health/", 220, 400),
    ("wiki/workflows/", 160, 280),
)

DIGEST_SKIP_DIRS = {".git", "__pycache__"}
SOURCE_DRIFT_MEMORY_PREFIXES = ("wiki/", "manifests/")
SOURCE_DRIFT_MEMORY_FILES = {"AGENTS.md", "CLAUDE.md", "README.md"}


@dataclass(frozen=True)
class Issue:
    severity: str
    check: str
    path: str
    message: str


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def normalize_repo_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def resolve_repo_path(root: Path, raw_path: str) -> Path:
    normalized = normalize_repo_path(raw_path)
    candidate = Path(normalized)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError("Path must stay inside the repository")

    resolved = (root / candidate).resolve()
    resolved.relative_to(root.resolve())
    return resolved


def iter_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for entry in MARKDOWN_ROOTS:
        path = root / entry
        if not path.exists():
            continue
        if path.is_file():
            if path.suffix.lower() in {".md", ".mdc"}:
                files.append(path)
            continue
        files.extend(
            p
            for p in path.rglob("*")
            if p.is_file() and p.suffix.lower() in {".md", ".mdc"}
        )
    return sorted(set(files))


def iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for entry in TEXT_ROOTS:
        path = root / entry
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
            continue
        files.extend(
            p
            for p in path.rglob("*")
            if p.is_file() and p.suffix.lower() in {".md", ".mdc", ".py", ".ps1", ".txt"}
        )
    return sorted(set(files))


def markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<"):
        end = target.find(">")
        if end != -1:
            target = target[1:end]
    else:
        target = target.split()[0]
    return unquote(target.strip())


def is_external_target(target: str) -> bool:
    return target.startswith(
        (
            "#",
            "http://",
            "https://",
            "mailto:",
            "tel:",
            "data:",
        )
    )


def check_broken_links(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in iter_markdown_files(root):
        in_fence = False
        for line in read_text(path).splitlines():
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_RE.finditer(line):
                target = markdown_target(match.group(1))
                if not target or is_external_target(target):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    issues.append(
                        Issue(
                            "error",
                            "broken-links",
                            rel(root, path),
                            f"Missing target: {target}",
                        )
                    )
    return issues


def check_log_format(root: Path) -> list[Issue]:
    path = root / "wiki" / "log.md"
    if not path.exists():
        return [Issue("error", "log-format", "wiki/log.md", "File is missing")]

    issues: list[Issue] = []
    in_fence = False
    for lineno, line in enumerate(read_text(path).splitlines(), start=1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line.startswith("## "):
            continue
        if line == "## Формат записи" or line.startswith("## YYYY-MM-DD | "):
            continue
        if not LOG_HEADING_RE.match(line):
            issues.append(
                Issue(
                    "error",
                    "log-format",
                    f"wiki/log.md:{lineno}",
                    "Heading must match 'YYYY-MM-DD | kind | short-title'",
                )
            )
    return issues


def check_old_paths(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in iter_text_files(root):
        for lineno, line in enumerate(read_text(path).splitlines(), start=1):
            if OLD_ROOT_PATH_RE.search(line):
                issues.append(
                    Issue(
                        "error",
                        "old-root-path",
                        f"{rel(root, path)}:{lineno}",
                        "Use the raw source layer instead of legacy root source paths",
                    )
                )
    return issues


def check_old_cycle_and_path_depth(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in iter_text_files(root):
        for lineno, line in enumerate(read_text(path).splitlines(), start=1):
            if OLD_CYCLE in line:
                issues.append(
                    Issue(
                        "error",
                        "old-cycle",
                        f"{rel(root, path)}:{lineno}",
                        "Use the triage-first cycle",
                    )
                )
            if OLD_DEPTH_EXPR in line:
                issues.append(
                    Issue(
                        "error",
                        "path-depth",
                        f"{rel(root, path)}:{lineno}",
                        "Check path depth after raw/ migration",
                    )
                )
    return issues


def check_wiki_asset_leakage(root: Path) -> list[Issue]:
    wiki = root / "wiki"
    if not wiki.exists():
        return []
    return [
        Issue(
            "error",
            "wiki-asset-leakage",
            rel(root, path),
            "Binary or asset-like file is stored in wiki/",
        )
        for path in sorted(wiki.rglob("*"))
        if path.is_file() and path.suffix.lower() in BINARY_EXTENSIONS
    ]


def catalog_targets(root: Path) -> set[Path]:
    index = root / "wiki" / "index.md"
    if not index.exists():
        return set()

    text = read_text(index)
    start = text.find("## Catalog")
    if start == -1:
        return set()
    end = text.find("\n## ", start + 1)
    section = text[start:] if end == -1 else text[start:end]
    targets: set[Path] = set()
    for match in LINK_RE.finditer(section):
        target = markdown_target(match.group(1)).split("#", 1)[0]
        if target and not is_external_target(target):
            targets.add((index.parent / target).resolve())
    return targets


def expected_catalog_pages(root: Path) -> set[Path]:
    wiki = root / "wiki"
    if not wiki.exists():
        return set()

    expected = {p.resolve() for p in wiki.glob("*.md") if p.name != "index.md"}
    expected.update(p.resolve() for p in wiki.glob("*/index.md"))
    return expected


def check_catalog_entries(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    index = root / "wiki" / "index.md"
    if not index.exists():
        return [Issue("error", "catalog", "wiki/index.md", "File is missing")]

    actual = catalog_targets(root)
    for path in sorted(expected_catalog_pages(root) - actual):
        issues.append(
            Issue(
                "error",
                "catalog",
                "wiki/index.md",
                f"Missing Catalog entry for {rel(root, path)}",
            )
        )
    return issues


def check_manifest_entries(root: Path) -> list[Issue]:
    path = root / "manifests" / "sources.md"
    if not path.exists():
        return [Issue("error", "manifest", "manifests/sources.md", "File is missing")]

    text = read_text(path)
    issues: list[Issue] = []
    for required in REQUIRED_MANIFEST_PATHS:
        if f"`{required}`" not in text:
            issues.append(
                Issue(
                    "error",
                    "manifest",
                    "manifests/sources.md",
                    f"Missing manifest entry for {required}",
                )
            )
    return issues


def check_obsidian_syntax(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in iter_markdown_files(root):
        for lineno, line in enumerate(read_text(path).splitlines(), start=1):
            if "[[" in line:
                issues.append(
                    Issue(
                        "error",
                        "obsidian-syntax",
                        f"{rel(root, path)}:{lineno}",
                        "Use standard Markdown links instead of Obsidian-only links",
                    )
                )
    return issues


def check_wiki_output_health_sections(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    checks = (
        (
            "wiki/outputs",
            OUTPUT_FILENAME_RE,
            "output-name",
            "Use YYYY-MM-DD-short-slug.md for output files",
        ),
        (
            "wiki/health",
            HEALTH_FILENAME_RE,
            "health-name",
            "Use YYYY-MM-DD-health.md or YYYY-MM-DD-health-scope.md for health reports",
        ),
    )
    for directory, pattern, check_name, message in checks:
        base = root / directory
        if not base.exists():
            continue
        for path in sorted(base.glob("*.md")):
            if path.name == "index.md":
                continue
            if not pattern.match(path.name):
                issues.append(Issue("error", check_name, rel(root, path), message))
    return issues


def page_budget_for(path: str) -> tuple[int, int]:
    for prefix, soft_limit, hard_limit in PAGE_BUDGETS:
        if path == prefix or path.startswith(prefix):
            return soft_limit, hard_limit
    return DEFAULT_WIKI_PAGE_SOFT_LIMIT, DEFAULT_WIKI_PAGE_HARD_LIMIT


def check_page_budget(root: Path) -> list[Issue]:
    wiki = root / "wiki"
    if not wiki.exists():
        return []

    issues: list[Issue] = []
    for path in sorted(wiki.rglob("*.md")):
        repo_path = rel(root, path)
        soft_limit, hard_limit = page_budget_for(repo_path)
        line_count = len(read_text(path).splitlines())
        if line_count > hard_limit:
            issues.append(
                Issue(
                    "error",
                    "page-budget",
                    repo_path,
                    f"{line_count} lines exceeds hard limit {hard_limit}; split or compact the page",
                )
            )
        elif line_count > soft_limit:
            issues.append(
                Issue(
                    "warning",
                    "page-budget",
                    repo_path,
                    f"{line_count} lines exceeds soft limit {soft_limit}; consider compaction",
                )
            )
    return issues


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_digest_tree_files(path: Path) -> list[Path]:
    files: list[Path] = []
    for child in path.rglob("*"):
        if not child.is_file():
            continue
        if any(part in DIGEST_SKIP_DIRS for part in child.relative_to(path).parts):
            continue
        files.append(child)
    return sorted(files)


def sha256_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for child in iter_digest_tree_files(path):
        digest.update(child.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(child).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def check_source_digests(root: Path) -> list[Issue]:
    manifest = root / SOURCE_DIGEST_MANIFEST
    if not manifest.exists():
        return []

    try:
        data = json.loads(read_text(manifest))
    except json.JSONDecodeError as error:
        return [
            Issue(
                "error",
                "source-digest",
                rel(root, manifest),
                f"Invalid JSON: {error.msg}",
            )
        ]

    issues: list[Issue] = []
    if not isinstance(data, dict):
        return [Issue("error", "source-digest", rel(root, manifest), "Manifest must be a JSON object")]
    if data.get("version") != 1:
        issues.append(
            Issue("error", "source-digest", rel(root, manifest), "Manifest version must be 1")
        )

    entries = data.get("entries", [])
    if not isinstance(entries, list):
        return issues + [
            Issue("error", "source-digest", rel(root, manifest), "Manifest entries must be a list")
        ]

    for index, entry in enumerate(entries, start=1):
        location = f"{rel(root, manifest)}:entries[{index}]"
        if not isinstance(entry, dict):
            issues.append(Issue("error", "source-digest", location, "Entry must be an object"))
            continue

        raw_path = entry.get("path")
        expected = entry.get("sha256")
        kind = entry.get("kind")

        if not isinstance(raw_path, str) or not raw_path:
            issues.append(Issue("error", "source-digest", location, "Entry path is required"))
            continue
        if not isinstance(expected, str) or not SHA256_RE.match(expected.lower()):
            issues.append(Issue("error", "source-digest", location, "Entry sha256 must be 64 hex chars"))
            continue
        if kind is not None and kind not in {"file", "tree"}:
            issues.append(Issue("error", "source-digest", location, "Entry kind must be file or tree"))
            continue

        try:
            source = resolve_repo_path(root, raw_path)
        except ValueError as error:
            issues.append(Issue("error", "source-digest", location, str(error)))
            continue

        if not source.exists():
            issues.append(Issue("error", "source-digest", location, f"Missing source: {raw_path}"))
            continue

        source_kind = kind or ("tree" if source.is_dir() else "file")
        if source_kind == "file" and not source.is_file():
            issues.append(Issue("error", "source-digest", location, f"Expected file: {raw_path}"))
            continue
        if source_kind == "tree" and not source.is_dir():
            issues.append(Issue("error", "source-digest", location, f"Expected directory: {raw_path}"))
            continue

        actual = sha256_file(source) if source_kind == "file" else sha256_tree(source)
        if actual != expected.lower():
            issues.append(
                Issue(
                    "error",
                    "source-digest",
                    location,
                    f"Source drift for {raw_path}; review wiki/writeback and update sha256",
                )
            )

    return issues


def git_staged_files(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "-c",
                "core.quotepath=false",
                "diff",
                "--cached",
                "--name-only",
                "--diff-filter=ACMR",
            ],
            check=False,
            capture_output=True,
            encoding="utf-8",
        )
    except (FileNotFoundError, OSError):
        return []
    if result.returncode != 0:
        return []
    return [normalize_repo_path(line) for line in result.stdout.splitlines() if line.strip()]


def is_source_change(path: str) -> bool:
    return path.startswith("raw/") and not path.endswith("/.gitkeep")


def is_memory_change(path: str) -> bool:
    return path in SOURCE_DRIFT_MEMORY_FILES or path.startswith(SOURCE_DRIFT_MEMORY_PREFIXES)


def check_staged_source_drift(root: Path) -> list[Issue]:
    staged = git_staged_files(root)
    if not staged:
        return []

    source_changes = sorted(path for path in staged if is_source_change(path))
    if not source_changes or any(is_memory_change(path) for path in staged):
        return []

    shown = ", ".join(source_changes[:5])
    if len(source_changes) > 5:
        shown += f", ... +{len(source_changes) - 5} more"
    return [
        Issue(
            "warning",
            "staged-source-drift",
            "git index",
            f"Staged raw source changed without staged wiki/manifest update: {shown}",
        )
    ]


def run_checks(root: Path) -> list[Issue]:
    checks = (
        check_broken_links,
        check_log_format,
        check_old_paths,
        check_old_cycle_and_path_depth,
        check_wiki_asset_leakage,
        check_catalog_entries,
        check_manifest_entries,
        check_obsidian_syntax,
        check_wiki_output_health_sections,
        check_page_budget,
        check_source_digests,
        check_staged_source_drift,
    )
    issues: list[Issue] = []
    for check in checks:
        issues.extend(check(root))
    return issues


def print_text_report(issues: list[Issue]) -> None:
    if not issues:
        print("wiki_lint: OK")
        return

    for issue in issues:
        print(f"{issue.severity.upper()} {issue.check} {issue.path}: {issue.message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a text report.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    issues = run_checks(root)
    if args.json:
        print(json.dumps([asdict(issue) for issue in issues], ensure_ascii=False, indent=2))
    else:
        print_text_report(issues)
    return 1 if any(issue.severity == "error" for issue in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
