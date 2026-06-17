param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [string]$Python = "C:\Users\Ancie\AppData\Local\Programs\Python\Python313\python.exe"
)

$ErrorActionPreference = "Stop"

if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Version must use semantic form like 0.2.0"
}

$initPath = "ancient_all_in_one\__init__.py"
$projectPath = "pyproject.toml"

(Get-Content $initPath -Raw) -replace '__version__ = "[^"]+"', "__version__ = `"$Version`"" | Set-Content $initPath
(Get-Content $projectPath -Raw) -replace 'version = "[^"]+"', "version = `"$Version`"" | Set-Content $projectPath

& $PSScriptRoot\check.ps1 -Python $Python

Write-Host "Version updated to $Version. Review the diff, then commit and tag:"
Write-Host "  git diff"
Write-Host "  git commit -am 'Release v$Version'"
Write-Host "  git tag v$Version"
Write-Host "  git push && git push origin v$Version"
Write-Host "Then create a GitHub release for v$Version."
