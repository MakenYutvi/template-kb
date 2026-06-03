param(
    [string] $Root = ".",
    [switch] $Force
)

$ErrorActionPreference = "Stop"

$PythonLauncher = Join-Path $PSScriptRoot "kb_python.ps1"
$Installer = Join-Path $PSScriptRoot "install_pre_commit.py"
$InstallerArgs = @($Installer, "--root", $Root)

if ($Force) {
    $InstallerArgs += "--force"
}

& $PythonLauncher @InstallerArgs
exit $LASTEXITCODE
