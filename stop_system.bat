@echo off
setlocal

echo Stopping SignalShop services...
docker compose -f docker/docker-compose.yml down
echo Services stopped.
pause
endlocal