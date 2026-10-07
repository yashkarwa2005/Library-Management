# =============================================================================
# ONE-CLICK GITHUB PROJECT & KANBAN SETUP SYSTEM (PowerShell Entrypoint)
# =============================================================================
# This script orchestrates environment checks, authentication verification,
# and invokes the setup engine to provision GitHub Scrum artifacts.
# =============================================================================

[CmdletBinding()]
param(
    [switch]$Yes,
    [switch]$NoBrowser,
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$ExtraArgs
)

$ErrorActionPreference = "Stop"

# Ensure UTF-8 output encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " ONE-CLICK GITHUB PROJECT & KANBAN SETUP (PowerShell)       " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..\..")

# 1. Check Python
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    $PythonCmd = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $PythonCmd) {
    Write-Host "[ERROR] Python 3 is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# 2. Check GitHub CLI
$GhCmd = Get-Command gh -ErrorAction SilentlyContinue
if (-not $GhCmd) {
    # Check default Windows paths
    $GhCandidates = @(
        "$env:ProgramFiles\GitHub CLI\gh.exe",
        "${env:ProgramFiles(x86)}\GitHub CLI\gh.exe",
        "$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe"
    )
    foreach ($cand in $GhCandidates) {
        if (Test-Path $cand) {
            $candDir = Split-Path -Parent $cand
            $env:Path = "$candDir;$env:Path"
            $GhCmd = Get-Command gh -ErrorAction SilentlyContinue
            break
        }
    }
}

if (-not $GhCmd) {
    Write-Host "[ERROR] GitHub CLI ('gh') is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Install options:" -ForegroundColor Yellow
    Write-Host "  1. Via Windows Package Manager: winget install --id GitHub.cli" -ForegroundColor Yellow
    Write-Host "  2. Official MSI Installer:     https://cli.github.com/" -ForegroundColor Yellow
    exit 1
}

# 3. Invoke Python setup engine
$SetupPy = Join-Path $ScriptDir "setup_project.py"
$pyArgs = @($SetupPy)

if ($Yes) {
    $pyArgs += "--yes"
}
if ($NoBrowser) {
    $pyArgs += "--no-browser"
}
if ($ExtraArgs) {
    $pyArgs += $ExtraArgs
}

Push-Location $ProjectRoot
try {
    & $PythonCmd.Source @pyArgs
}
finally {
    Pop-Location
}
