param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $PythonArgs
)

$ErrorActionPreference = "Stop"

function New-PythonCandidate {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Command,
        [string[]] $PrefixArgs = @()
    )

    [PSCustomObject]@{
        Command = $Command
        PrefixArgs = $PrefixArgs
    }
}

function Test-PythonCandidate {
    param(
        [Parameter(Mandatory = $true)]
        $Candidate
    )

    $Command = $Candidate.Command
    if (!$Command) {
        return $false
    }

    if (!(Test-Path -LiteralPath $Command) -and !(Get-Command $Command -ErrorAction SilentlyContinue)) {
        return $false
    }

    & $Command @($Candidate.PrefixArgs) -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" 1>$null 2>$null
    return $LASTEXITCODE -eq 0
}

$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$Candidates = @()

if ($env:KB_PYTHON) {
    $Candidates += New-PythonCandidate $env:KB_PYTHON
}

if ($env:CODEX_PYTHON) {
    $Candidates += New-PythonCandidate $env:CODEX_PYTHON
}

$Candidates += New-PythonCandidate (Join-Path $RepoRoot ".venv\Scripts\python.exe")
$Candidates += New-PythonCandidate (Join-Path $RepoRoot ".venv\bin\python")
$Candidates += New-PythonCandidate (Join-Path $RepoRoot ".codex_runtime\python\python.exe")

if ($env:USERPROFILE) {
    $Candidates += New-PythonCandidate (Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe")
}

$Candidates += New-PythonCandidate "python"
$Candidates += New-PythonCandidate "python3"
$Candidates += New-PythonCandidate "py" @("-3")

foreach ($Candidate in $Candidates) {
    if (!(Test-PythonCandidate $Candidate)) {
        continue
    }

    if (!$PythonArgs -or $PythonArgs.Count -eq 0) {
        Write-Output $Candidate.Command
        exit 0
    }

    # Python uses the Windows ANSI code page for redirected streams by default.
    # Use UTF-8 when the caller has not chosen a stream encoding. An explicit
    # PYTHONIOENCODING overrides -X utf8: preserve the caller's Python options
    # and matching decoder too (including -E/-I, which ignore the environment).
    # A value such as ':replace' selects only an error handler, not a codec.
    $PreviousConsoleEncoding = [Console]::OutputEncoding
    try {
        $StreamEncoding = ($env:PYTHONIOENCODING -split ':', 2)[0]
        $Utf8Args = @()
        if (!$StreamEncoding) {
            [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
            $Utf8Args = @('-X', 'utf8')
        }
        & $Candidate.Command @($Candidate.PrefixArgs) @Utf8Args @PythonArgs
        $PythonExitCode = $LASTEXITCODE
    }
    finally {
        [Console]::OutputEncoding = $PreviousConsoleEncoding
    }
    exit $PythonExitCode
}

Write-Error "Could not find a working Python 3.10+ runtime. Set KB_PYTHON to a Python executable path."
exit 1
