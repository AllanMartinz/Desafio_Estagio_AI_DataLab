@echo off
color 0A
echo ===========================================
echo   EXTRATOR DE LAUDOS - VERSAO NUVEM (Gemini)
echo ===========================================
echo.
pip install pandas openpyxl google-genai -q
python extracao_nuvem.py
echo.
pause