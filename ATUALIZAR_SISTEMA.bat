@echo off
title CNAB Coopluiza - Atualizando sistema
color 0B

echo ============================================================
echo   CNAB Coopluiza - Atualizando sistema...
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/3] Baixando atualizacoes do git...
git pull
echo.

echo [2/3] Instalando novas dependencias (se houver)...
pip install -r requirements.txt -q
echo.

echo [3/3] Pronto! Reinicie o servidor para aplicar as mudancas.
echo.
echo   Execute INICIAR_SERVIDOR.bat para reiniciar.
echo ============================================================
pause
