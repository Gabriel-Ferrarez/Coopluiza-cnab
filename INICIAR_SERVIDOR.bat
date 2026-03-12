@echo off
title CNAB Coopluiza - Servidor
color 0A

echo ============================================================
echo   CNAB Coopluiza - Iniciando servidor...
echo ============================================================
echo.

:: Pega o IP local automaticamente
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    goto :found
)
:found
set IP=%IP:~1%

echo   Servidor rodando em:
echo   - Local:    http://localhost:8000/app
echo   - Rede:     http://%IP%:8000/app
echo.
echo   Mande o link da REDE para o time acessar!
echo   Pressione CTRL+C para parar o servidor.
echo ============================================================
echo.

cd /d "%~dp0backend"
python main.py
pause
