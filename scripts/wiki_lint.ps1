param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $LintArgs
)

$ErrorActionPreference = "Stop"

$PythonLauncher = Join-Path $PSScriptRoot "kb_python.ps1"
$WikiLint = Join-Path $PSScriptRoot "wiki_lint.py"

if (!(Test-Path -LiteralPath $WikiLint)) {
    Write-Error "scripts/wiki_lint.py not found."
    exit 1
}

& $PythonLauncher $WikiLint @LintArgs
exit $LASTEXITCODE
