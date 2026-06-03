param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $ItemArgs
)

$ErrorActionPreference = "Stop"

$PythonLauncher = Join-Path $PSScriptRoot "kb_python.ps1"
$NewItem = Join-Path $PSScriptRoot "new_kb_item.py"

if (!(Test-Path -LiteralPath $NewItem)) {
    Write-Error "scripts/new_kb_item.py not found."
    exit 1
}

& $PythonLauncher $NewItem @ItemArgs
exit $LASTEXITCODE
