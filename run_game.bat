@echo off
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    echo Starting Management and Organization Concepts Review Games...
    ".venv\Scripts\python.exe" src\main.py
) else (
    echo .venv not found.
    echo Create it with:
    echo   py -m venv .venv
    echo   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    echo Then run this file again.
    pause #py -3.11 .\src\main.py
)
