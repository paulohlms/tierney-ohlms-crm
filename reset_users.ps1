# PowerShell script to reset admin users
# Run this from PowerShell: .\reset_users.ps1

$url = "https://tierney-ohlms-crm.onrender.com/admin/reset-users"

Write-Host "Calling reset endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $url -Method GET -UseBasicParsing
    Write-Host "Response received:" -ForegroundColor Green
    Write-Host $response.Content
} catch {
    Write-Host "Error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response body: $responseBody"
    }
}

