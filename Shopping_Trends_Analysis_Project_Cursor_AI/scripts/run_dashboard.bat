@echo off
setlocal

set STREAMLIT_EXE=%APPDATA%\Python\Python313\Scripts\streamlit.exe
if not exist "%STREAMLIT_EXE%" (
  echo Could not find streamlit.exe at %STREAMLIT_EXE%
  echo Try: python -m pip install streamlit
  exit /b 1
)

REM Start Streamlit on port 8502
start "Streamlit Dashboard" "%STREAMLIT_EXE%" run app/dashboard.py --server.headless true --server.port 8502

REM Give the server a moment to start
ping -n 3 127.0.0.1 > nul

REM Open default browser to the dashboard
start http://localhost:8502/

endlocal






