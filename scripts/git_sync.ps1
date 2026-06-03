param(
    # Named-only on purpose: $MessageParts owns position 0, so an inline message
    # is not mis-bound to $MessageFile. Use -MessageFile for multiline messages.
    [string] $MessageFile,
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]] $MessageParts
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Fail([string] $Message, [int] $Code = 1) {
    Write-Error $Message
    exit $Code
}

function Run-Command([string] $Exe, [string[]] $CommandArgs) {
    # Do not name this parameter $Args: it collides with the automatic $args
    # variable, so @Args would splat the (empty) automatic value and invoke the
    # executable with no arguments.
    & $Exe @CommandArgs
    if ($LASTEXITCODE -ne 0) {
        Fail "$Exe $($CommandArgs -join ' ') failed with exit code $LASTEXITCODE."
    }
}

function Ensure-NoGitOperationInProgress([string] $GitDir) {
    $markers = @(
        "MERGE_HEAD",
        "CHERRY_PICK_HEAD",
        "REVERT_HEAD",
        "rebase-apply",
        "rebase-merge"
    )

    foreach ($marker in $markers) {
        $path = Join-Path $GitDir $marker
        if (Test-Path -LiteralPath $path) {
            Fail "Git operation in progress ($marker). Resolve it before running git_sync."
        }
    }
}

function Get-StagedBlockedFiles([string[]] $Files) {
    $blocked = New-Object System.Collections.Generic.List[string]

    foreach ($file in $Files) {
        $normalized = $file -replace "\\", "/"

        $isPlaintextSecret =
            $normalized -match "(^|/)\.env($|\.)" -or
            $normalized -match "\.agekey$" -or
            $normalized -match "(^|/)age-key\.txt$" -or
            $normalized -match "(^|/)keys\.txt$" -or
            ($normalized -match "^secrets/" -and $normalized -notmatch "\.enc\.(env|json|ya?ml)$")

        $isGeneratedOrLock =
            $normalized -match "^outputs/" -or
            $normalized -match "(^|/)~\$"

        if ($isPlaintextSecret -or $isGeneratedOrLock) {
            $blocked.Add($file)
        }
    }

    return $blocked.ToArray()
}

# Resolve the commit message. A multiline message cannot survive the cmd.exe
# `%*` boundary: cmd truncates a command-line argument at the first newline, so
# the body is silently lost. Provide two newline-safe channels that bypass the
# command line, plus the inline single-line form:
#   1. -MessageFile <path>     -> file content (preferred for multiline)
#   2. $env:GIT_SYNC_MESSAGE   -> env survives the cmd->powershell boundary intact
#   3. inline arguments        -> joined into a single-line message
# Precedence: -MessageFile, then $env:GIT_SYNC_MESSAGE, then inline arguments.
# The resolved message is committed with an in-process `git commit -m`, which
# carries embedded newlines intact (only the cmd command line truncates them).
$message = $null

if ($MessageFile) {
    if (!(Test-Path -LiteralPath $MessageFile -PathType Leaf)) {
        Fail "Message file not found: $MessageFile"
    }
    # Strip a leading UTF-8 BOM: PS 5.1 `Set-Content -Encoding utf8` writes one,
    # and it would otherwise leak into the commit subject line.
    $message = ((Get-Content -Raw -LiteralPath $MessageFile) -replace "^\uFEFF", "").Trim()
}
elseif ($env:GIT_SYNC_MESSAGE) {
    $message = $env:GIT_SYNC_MESSAGE.Trim()
}
else {
    $message = ($MessageParts -join " ").Trim()
}

if (-not $message) {
    Write-Host "Usage: .\scripts\git_sync.cmd ""Commit message"""
    Write-Host "Multiline message: .\scripts\git_sync.cmd -MessageFile path\to\msg.txt"
    Write-Host "                or: set GIT_SYNC_MESSAGE env var, then run git_sync with no message."
    Write-Host "Runs: git add -A, wiki lint, staged whitespace check, commit, git pull --rebase, git push."
    exit 2
}

$repoRoot = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) {
    Fail "Not inside a Git repository."
}

$repoRoot = $repoRoot.Trim()
Set-Location $repoRoot

$gitDir = (& git rev-parse --git-dir).Trim()
Ensure-NoGitOperationInProgress $gitDir

$branch = (& git branch --show-current).Trim()
if (-not $branch) {
    Fail "Detached HEAD is not supported by git_sync."
}

$upstream = (& git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $upstream) {
    Fail "Current branch '$branch' has no upstream. Set upstream before running git_sync."
}
$upstream = $upstream.Trim()

Write-Host "[git-sync] Repository: $repoRoot"
Write-Host "[git-sync] Branch: $branch -> $upstream"
Write-Host "[git-sync] Current status:"
Run-Command -Exe "git" -CommandArgs @("status", "--short", "--branch")

$porcelain = @(git status --porcelain)
if ($porcelain.Count -eq 0) {
    Write-Host "[git-sync] No local changes. Pulling with rebase and pushing pending commits, if any."
    Run-Command -Exe "git" -CommandArgs @("pull", "--rebase")
    Run-Command -Exe "git" -CommandArgs @("push")
    exit 0
}

Run-Command -Exe "git" -CommandArgs @("add", "-A")

$stagedFiles = @(git diff --cached --name-only)
if ($stagedFiles.Count -eq 0) {
    Write-Host "[git-sync] No staged changes after git add -A. Pulling with rebase and pushing pending commits, if any."
    Run-Command -Exe "git" -CommandArgs @("pull", "--rebase")
    Run-Command -Exe "git" -CommandArgs @("push")
    exit 0
}

# Wrap in @(): an empty array returned from the function unrolls to $null,
# and $null.Count throws under Set-StrictMode -Version Latest.
$blockedFiles = @(Get-StagedBlockedFiles $stagedFiles)
if ($blockedFiles.Count -gt 0) {
    Write-Host "[git-sync] Refusing to commit blocked files:"
    foreach ($file in $blockedFiles) {
        Write-Host "  - $file"
    }
    Fail "Review .gitignore or unstage blocked files before running git_sync."
}

Write-Host "[git-sync] Staged changes:"
Run-Command -Exe "git" -CommandArgs @("diff", "--cached", "--stat")

$wikiLint = Join-Path $PSScriptRoot "wiki_lint.ps1"
if (!(Test-Path -LiteralPath $wikiLint)) {
    Fail "scripts/wiki_lint.ps1 not found."
}

Write-Host "[git-sync] Running wiki_lint."
& $wikiLint
if ($LASTEXITCODE -ne 0) {
    Fail "wiki_lint failed with exit code $LASTEXITCODE."
}

Write-Host "[git-sync] Running staged whitespace check."
Run-Command -Exe "git" -CommandArgs @("diff", "--cached", "--check")

Write-Host "[git-sync] Creating commit."
Run-Command -Exe "git" -CommandArgs @("commit", "-m", $message)

Write-Host "[git-sync] Pulling with rebase before push."
Run-Command -Exe "git" -CommandArgs @("pull", "--rebase")

Write-Host "[git-sync] Pushing."
Run-Command -Exe "git" -CommandArgs @("push")

Write-Host "[git-sync] Done."
