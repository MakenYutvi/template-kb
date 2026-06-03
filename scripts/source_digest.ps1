param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $DigestArgs
)

$ErrorActionPreference = "Stop"

$PythonLauncher = Join-Path $PSScriptRoot "kb_python.ps1"
$Digest = Join-Path $PSScriptRoot "source_digest.py"

if (!(Test-Path -LiteralPath $Digest)) {
    Write-Error "scripts/source_digest.py not found."
    exit 1
}

& $PythonLauncher $Digest @DigestArgs
exit $LASTEXITCODE
