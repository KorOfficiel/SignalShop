@echo off
setlocal

echo ==========================================
echo  SignalShop - Désinstallation
echo ==========================================
echo.

echo Arrêt des conteneurs et suppression des volumes...
docker compose -f docker/docker-compose.yml down -v

echo Suppression des fichiers générés...
if exist .env del .env
if exist dist rmdir /S /Q dist
if exist build rmdir /S /Q build
if exist SignalShop_Installer.spec del SignalShop_Installer.spec

echo Désinstallation terminée.
pause
endlocal