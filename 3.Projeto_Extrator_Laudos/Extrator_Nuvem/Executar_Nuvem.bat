@echo off
chcp 65001 > nul
set PYTHONUTF8=1
color 0A
echo ===========================================
echo   EXTRATOR DE LAUDOS - VERSAO NUVEM (Gemini)
echo ===========================================
echo.
pip install pandas openpyxl google-genai -q
python extracao_nuvem.py
echo.
pause