param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $DoctorArgs
)

$ErrorActionPreference = "Stop"

$PythonLauncher = Join-Path $PSScriptRoot "kb_python.ps1"
$Doctor = Join-Path $PSScriptRoot "kb_doctor.py"

if (!(Test-Path -LiteralPath $Doctor)) {
    Write-Error "scripts/kb_doctor.py not found."
    exit 1
}

& $PythonLauncher $Doctor @DoctorArgs
exit $LASTEXITCODE
