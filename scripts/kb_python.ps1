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

    & $Candidate.Command @($Candidate.PrefixArgs) @PythonArgs
    exit $LASTEXITCODE
}

Write-Error "Could not find a working Python 3.10+ runtime. Set KB_PYTHON to a Python executable path."
exit 1
