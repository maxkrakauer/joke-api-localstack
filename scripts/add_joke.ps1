param (
    [string]$ApiUrl
)

# Try to load last used API URL from .last_api_url at project root
$projectRoot = Resolve-Path "$PSScriptRoot\.."
$apiFilePath = Join-Path $projectRoot ".last_api_url"

if (-not $ApiUrl -and (Test-Path $apiFilePath)) {
    $savedUrl = Get-Content $apiFilePath -Raw
    if ($savedUrl) {
        $ApiUrl = $savedUrl.Trim()
        Write-Host "Using API URL from .last_api_url:"
        Write-Host "$ApiUrl`n"
    }
}

# If still no URL, ask the user
if (-not $ApiUrl) {
    Write-Host "Enter your API URL (e.g. http://localhost:4566/restapis/ABC123/dev/_user_request_/jokes):"
    $ApiUrl = Read-Host
}

Write-Host "Using API URL: $ApiUrl"

while ($true) {
    Write-Host "`nEnter joke text (or type 'exit' to quit):"
    $text = Read-Host

    if ($text -eq 'exit') {
        Write-Host "Goodbye!"
        break
    }

    Write-Host "Enter tags (comma-separated, e.g., programming,java):"
    $tags = Read-Host

    $tagsArray = $tags -split ',' | ForEach-Object { $_.Trim() }

    $bodyObject = @{
        text = $text
        tags = $tagsArray
    }

    $jsonBody = $bodyObject | ConvertTo-Json

    Write-Host "`nSending joke..."
    try {
        $response = Invoke-WebRequest -Uri $ApiUrl -Method POST -ContentType "application/json" -Body $jsonBody
        Write-Host "`nResponse status code: " $response.StatusCode
        Write-Host "Response body:"
        Write-Host $response.Content
    }
    catch {
        Write-Host "`nError sending request:"
        Write-Host $_
    }
}
