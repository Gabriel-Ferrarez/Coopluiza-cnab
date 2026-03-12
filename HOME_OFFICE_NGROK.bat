@echo off
title CNAB Coopluiza - Home Office (ngrok)
color 0E

echo ============================================================
echo   CNAB Coopluiza - Modo Home Office
echo ============================================================
echo.
echo   Este script inicia o servidor E o ngrok juntos.
echo   Uma URL publica sera gerada para o time acessar.
echo.
echo   PRE-REQUISITO: ngrok instalado e configurado.
echo   Download: https://ngrok.com/download
echo ============================================================
echo.

:: Inicia o servidor em background
start "Servidor CNAB" cmd /k "cd /d "%~dp0backend" && python main.py"

:: Aguarda 3 segundos para o servidor subir
timeout /t 3 /nobreak > nul

:: Inicia o ngrok
echo Iniciando ngrok...
echo.
echo Mande esse link para o time acessar:
echo https://nonfanatical-delinda-toothlessly.ngrok-free.dev/app
echo.
ngrok http --url nonfanatical-delinda-toothlessly.ngrok-free.dev 8000
pause