param (
    [string]$ApiUrl
)

# Try to read last API URL if not given
$projectRoot = Resolve-Path "$PSScriptRoot\.."
$apiFilePath = Join-Path $projectRoot ".last_api_url"

if (-not $ApiUrl -and (Test-Path $apiFilePath)) {
    $ApiUrl = (Get-Content $apiFilePath -Raw).Trim()
    Write-Host "Using API URL from .last_api_url:"
    Write-Host "$ApiUrl`n"
}

# If still missing, ask for it
if (-not $ApiUrl) {
    Write-Host "Enter API URL:"
    $ApiUrl = Read-Host
}

Write-Host "`nFetching random joke..."
$response = curl.exe -s $ApiUrl

Write-Host "`nResponse:"
Write-Host $response
