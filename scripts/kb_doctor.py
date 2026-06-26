#!/usr/bin/env python3
"""Run a local health check for a template-kb repository."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CHANGELOG.md",
    "LICENSE",
    "SECURITY.md",
    "ROADMAP.md",
    "SETUP.md",
    ".ai/contract.md",
    ".ai/privacy.md",
    ".ai/tool-profiles/claude.md",
    "wiki/index.md",
    "wiki/current-status.md",
    "wiki/schema.md",
    "wiki/outputs/index.md",
    "wiki/health/index.md",
    "wiki/people/_template.md",
    "wiki/people/index.md",
    "wiki/workflows/output.md",
    "wiki/workflows/golden-eval.md",
    "wiki/workflows/meeting-ingest.md",
    "wiki/workflows/writeback.md",
    "indexes/meetings.md",
    "indexes/people-relations.md",
    "manifests/sources.md",
    "manifests/source-digests.json",
    "prompts/apply-template-upgrade.md",
    "docs/demo-walkthrough.md",
    "scripts/wiki_lint.py",
    "scripts/new_kb_item.py",
    "scripts/prune_os_scripts.py",
)

SECRET_PATH_RE = re.compile(
    r"(^|/)(\.env($|\.)|age-key\.txt$|keys\.txt$|id_rsa$|id_ed25519$)"
    r"|(\.agekey$|\.pem$|\.key$|\.p12$|\.pfx$)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Check:
    status: str
    name: str
    message: str


def run(args: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=root,
        check=False,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def git_output(root: Path, *args: str) -> str | None:
    result = run(["git", *args], root)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def normalize(path: str) -> str:
    return path.replace("\\", "/").strip()


def check_required_files(root: Path) -> list[Check]:
    missing = [path for path in REQUIRED_FILES if not (root / path).exists()]
    if missing:
        return [Check("ERROR", "required-files", "Missing: " + ", ".join(missing))]
    return [Check("OK", "required-files", "All required template files are present.")]


def check_git(root: Path) -> list[Check]:
    checks: list[Check] = []
    inside = git_output(root, "rev-parse", "--is-inside-work-tree")
    if inside != "true":
        return [Check("ERROR", "git", "Not inside a Git repository.")]

    checks.append(Check("OK", "git", "Repository detected."))

    branch = git_output(root, "branch", "--show-current")
    if branch:
        checks.append(Check("OK", "git-branch", f"Current branch: {branch}."))
    else:
        checks.append(Check("WARN", "git-branch", "Detached HEAD or branch name unavailable."))

    upstream = git_output(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if upstream:
        checks.append(Check("OK", "git-upstream", f"Upstream: {upstream}."))
    else:
        checks.append(Check("WARN", "git-upstream", "No upstream configured for current branch."))

    name = git_output(root, "config", "--get", "user.name")
    email = git_output(root, "config", "--get", "user.email")
    if name and email:
        checks.append(Check("OK", "git-identity", f"Git author: {name} <{email}>."))
    else:
        checks.append(Check("WARN", "git-identity", "Git user.name/user.email are not configured."))

    status = git_output(root, "status", "--porcelain")
    if status:
        checks.append(Check("WARN", "git-status", "Working tree has local changes."))
    else:
        checks.append(Check("OK", "git-status", "Working tree is clean."))

    return checks


def check_python() -> list[Check]:
    version = sys.version_info
    text = f"{version.major}.{version.minor}.{version.micro}"
    if version >= (3, 10):
        return [Check("OK", "python", f"Python runtime: {text}.")]
    return [Check("ERROR", "python", f"Python 3.10+ required, found {text}.")]


def check_os_scripts(root: Path) -> list[Check]:
    if not sys.platform.startswith("win"):
        return [Check("OK", "os-scripts", "Python entrypoints are available for macOS/Linux.")]

    required = (
        "scripts/kb_python.ps1",
        "scripts/wiki_lint.cmd",
        "scripts/wiki_lint.ps1",
        "scripts/kb_doctor.cmd",
        "scripts/kb_doctor.ps1",
        "scripts/prune_os_scripts.cmd",
        "scripts/prune_os_scripts.ps1",
    )
    missing = [path for path in required if not (root / path).exists()]
    if missing:
        return [Check("WARN", "os-scripts", "Missing Windows wrappers: " + ", ".join(missing))]
    return [Check("OK", "os-scripts", "Windows wrappers are present.")]


def check_pre_commit(root: Path) -> list[Check]:
    hook_path = git_output(root, "rev-parse", "--git-path", "hooks/pre-commit")
    if not hook_path:
        return [Check("WARN", "pre-commit", "Could not resolve Git hook path.")]

    path = Path(hook_path)
    if not path.is_absolute():
        path = root / path
    if not path.exists():
        return [Check("WARN", "pre-commit", "Pre-commit hook is not installed.")]

    text = path.read_text(encoding="utf-8", errors="ignore")
    if "template-kb generated pre-commit hook" in text:
        return [Check("OK", "pre-commit", "template-kb pre-commit hook is installed.")]
    return [Check("WARN", "pre-commit", "A pre-commit hook exists but was not generated by template-kb.")]


def check_wiki_lint(root: Path) -> list[Check]:
    script = root / "scripts" / "wiki_lint.py"
    if not script.exists():
        return [Check("ERROR", "wiki-lint", "scripts/wiki_lint.py is missing.")]

    result = run([sys.executable, str(script)], root)
    output = (result.stdout + result.stderr).strip()
    if result.returncode == 0:
        return [Check("OK", "wiki-lint", output or "wiki_lint passed.")]
    return [Check("ERROR", "wiki-lint", output or "wiki_lint failed.")]


def list_git_files(root: Path, tracked: bool) -> list[str]:
    args = ["git", "ls-files"] if tracked else ["git", "ls-files", "--others", "--exclude-standard"]
    result = run(args, root)
    if result.returncode != 0:
        return []
    return [normalize(line) for line in result.stdout.splitlines() if line.strip()]


def check_plaintext_secret_paths(root: Path) -> list[Check]:
    allowed = {".env.example"}
    tracked = [
        path
        for path in list_git_files(root, tracked=True)
        if path not in allowed and SECRET_PATH_RE.search(path)
    ]
    untracked = [
        path
        for path in list_git_files(root, tracked=False)
        if path not in allowed and SECRET_PATH_RE.search(path)
    ]

    checks: list[Check] = []
    if tracked:
        checks.append(Check("ERROR", "secret-paths", "Tracked secret-like files: " + ", ".join(tracked[:10])))
    else:
        checks.append(Check("OK", "secret-paths", "No tracked plaintext secret-like paths found."))

    if untracked:
        checks.append(Check("WARN", "untracked-secret-paths", "Untracked secret-like files exist: " + ", ".join(untracked[:10])))
    return checks


def run_checks(root: Path) -> list[Check]:
    checks: list[Check] = []
    checks.extend(check_required_files(root))
    checks.extend(check_git(root))
    checks.extend(check_python())
    checks.extend(check_os_scripts(root))
    checks.extend(check_pre_commit(root))
    checks.extend(check_wiki_lint(root))
    checks.extend(check_plaintext_secret_paths(root))
    return checks


def print_report(checks: list[Check]) -> None:
    for check in checks:
        print(f"{check.status} {check.name}: {check.message}")

    errors = sum(1 for check in checks if check.status == "ERROR")
    warnings = sum(1 for check in checks if check.status == "WARN")
    print(f"\nSummary: {errors} error(s), {warnings} warning(s).")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    checks = run_checks(root)
    if args.json:
        print(json.dumps([asdict(check) for check in checks], ensure_ascii=False, indent=2))
    else:
        print_report(checks)
    return 1 if any(check.status == "ERROR" for check in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
