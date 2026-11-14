@echo off
title RecruMatch Server
cd /d "%~dp0"
echo ========================================================
echo   Starting RecruMatch - AI Resume Screening Tool...
echo ========================================================
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\streamlit.exe" (
    echo Activating virtual environment and launching Streamlit...
    echo URL: http://localhost:8501
    echo.
    .\.venv\Scripts\streamlit.exe run app.py
) else (
    echo Virtual environment not found. Attempting global streamlit...
    streamlit run app.py
)

pause
