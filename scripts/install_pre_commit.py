#!/usr/bin/env python3
"""Install the local Git pre-commit hook for a personal knowledge base."""

from __future__ import annotations

import argparse
import shutil
import stat
import subprocess
import sys
from pathlib import Path


MARKER = "template-kb generated pre-commit hook"


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def hook_paths(root: Path) -> tuple[Path, Path, Path]:
    shell_hook = Path(run_git(["rev-parse", "--git-path", "hooks/pre-commit"], root))
    ps_hook = Path(run_git(["rev-parse", "--git-path", "hooks/pre-commit.ps1"], root))
    local_ps_hook = Path(run_git(["rev-parse", "--git-path", "hooks/pre-commit.local.ps1"], root))

    if not shell_hook.is_absolute():
        shell_hook = root / shell_hook
    if not ps_hook.is_absolute():
        ps_hook = root / ps_hook
    if not local_ps_hook.is_absolute():
        local_ps_hook = root / local_ps_hook
    return shell_hook, ps_hook, local_ps_hook


def is_generated(path: Path) -> bool:
    return path.exists() and MARKER in path.read_text(encoding="utf-8", errors="ignore")


def preserve_existing_ps_hook(ps_hook: Path, local_ps_hook: Path, force: bool) -> None:
    if not ps_hook.exists() or is_generated(ps_hook):
        return

    if local_ps_hook.exists() and not force:
        raise SystemExit(
            f"{local_ps_hook} already exists and {ps_hook} is not generated. "
            "Resolve manually or rerun with --force."
        )

    local_ps_hook.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ps_hook, local_ps_hook)
    print(f"Preserved existing PowerShell hook: {local_ps_hook}")


def write_shell_hook(path: Path) -> None:
    content = f"""#!/bin/sh
# {MARKER}

repo_root="$(git rev-parse --show-toplevel)" || exit 1
ps_hook="$(git rev-parse --git-path hooks/pre-commit.ps1)"

if command -v powershell.exe >/dev/null 2>&1 && [ -f "$ps_hook" ]; then
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$ps_hook"
    exit $?
fi

if command -v python3 >/dev/null 2>&1; then
    python3 "$repo_root/scripts/wiki_lint.py"
    exit $?
fi

if command -v python >/dev/null 2>&1; then
    python "$repo_root/scripts/wiki_lint.py"
    exit $?
fi

echo "Could not find powershell.exe, python3 or python for scripts/wiki_lint.py." >&2
exit 1
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    current_mode = path.stat().st_mode
    path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def write_ps_hook(path: Path, installer_python: Path) -> None:
    installer_python_text = installer_python.as_posix()
    content = f"""# {MARKER}
$ErrorActionPreference = "Stop"

function Fail($Message) {{
    Write-Error $Message
    exit 1
}}

function Invoke-WikiLint($RepoRoot) {{
    $WikiLint = Join-Path $RepoRoot "scripts\\wiki_lint.py"
    if (!(Test-Path -LiteralPath $WikiLint)) {{
        Fail "scripts/wiki_lint.py not found."
    }}

    $WikiLintPs1 = Join-Path $RepoRoot "scripts\\wiki_lint.ps1"
    if (Test-Path -LiteralPath $WikiLintPs1) {{
        & $WikiLintPs1
        if ($LASTEXITCODE -ne 0) {{
            exit $LASTEXITCODE
        }}
        return
    }}

    $Candidates = @()
    $InstallerPython = {ps_quote(installer_python_text)}
    if ($InstallerPython -and (Test-Path -LiteralPath $InstallerPython)) {{
        $Candidates += ,@($InstallerPython)
    }}
    if ($env:KB_PYTHON) {{
        $Candidates += ,@($env:KB_PYTHON)
    }}
    if ($env:CODEX_PYTHON) {{
        $Candidates += ,@($env:CODEX_PYTHON)
    }}
    $Candidates += ,@(Join-Path $RepoRoot ".venv\\Scripts\\python.exe")
    $Candidates += ,@(Join-Path $RepoRoot ".venv\\bin\\python")
    $Candidates += ,@(Join-Path $RepoRoot ".codex_runtime\\python\\python.exe")
    if ($env:USERPROFILE) {{
        $Candidates += ,@(Join-Path $env:USERPROFILE ".cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe")
    }}
    $Candidates += ,@("python")
    $Candidates += ,@("python3")
    $Candidates += ,@("py", "-3")

    foreach ($Candidate in $Candidates) {{
        $Command = $Candidate[0]
        $Args = @()
        if ($Candidate.Count -gt 1) {{
            $Args = $Candidate[1..($Candidate.Count - 1)]
        }}

        if (!(Get-Command $Command -ErrorAction SilentlyContinue) -and !(Test-Path -LiteralPath $Command)) {{
            continue
        }}

        & $Command @Args $WikiLint
        if ($LASTEXITCODE -eq 0) {{
            return
        }}
        if ($LASTEXITCODE -ne 9009) {{
            exit $LASTEXITCODE
        }}
    }}

    Fail "Could not find a working Python runtime for scripts/wiki_lint.py."
}}

$RepoRoot = (& git rev-parse --show-toplevel).Trim()
if (!$RepoRoot) {{
    Fail "Could not determine repository root."
}}

Invoke-WikiLint $RepoRoot

$LocalHook = Join-Path $PSScriptRoot "pre-commit.local.ps1"
if (Test-Path -LiteralPath $LocalHook) {{
    & $LocalHook
    if ($LASTEXITCODE -ne 0) {{
        exit $LASTEXITCODE
    }}
}}

exit 0
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def install(root: Path, force: bool) -> None:
    root = root.resolve()
    shell_hook, ps_hook, local_ps_hook = hook_paths(root)
    preserve_existing_ps_hook(ps_hook, local_ps_hook, force)
    write_shell_hook(shell_hook)
    write_ps_hook(ps_hook, Path(sys.executable).resolve())
    print(f"Installed pre-commit hook: {shell_hook}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--force", action="store_true", help="Overwrite pre-commit.local.ps1 if needed.")
    args = parser.parse_args(argv)

    install(Path(args.root), args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
