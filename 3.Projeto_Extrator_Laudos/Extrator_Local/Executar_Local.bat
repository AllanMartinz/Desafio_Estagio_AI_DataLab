@echo off
color 0B
echo ===========================================
echo   EXTRATOR DE LAUDOS - VERSAO LOCAL (Ollama)
echo ===========================================
echo.
pip install pandas openpyxl ollama -q
python extracao_local.py
echo.
pause