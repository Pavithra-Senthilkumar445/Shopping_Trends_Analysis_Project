param(
  [int]$Port = 8502
)

$streamlit = "$env:APPDATA\Python\Python313\Scripts\streamlit.exe"
if (-not (Test-Path $streamlit)) {
  Write-Error "Could not find streamlit.exe at $streamlit. Try: python -m pip install streamlit"
  exit 1
}

Start-Process -FilePath $streamlit -ArgumentList @('run','app/dashboard.py','--server.headless','true','--server.port',"$Port")
Start-Sleep -Seconds 3
Start-Process "http://localhost:$Port/"






