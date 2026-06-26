param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $PruneArgs
)

$ErrorActionPreference = "Stop"

$PythonLauncher = Join-Path $PSScriptRoot "kb_python.ps1"
$PruneScript = Join-Path $PSScriptRoot "prune_os_scripts.py"

if (!(Test-Path -LiteralPath $PruneScript)) {
    Write-Error "scripts/prune_os_scripts.py not found."
    exit 1
}

& $PythonLauncher $PruneScript @PruneArgs
exit $LASTEXITCODE
