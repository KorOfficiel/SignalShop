@echo off
setlocal EnableExtensions

echo.
echo  Starting SignalShop system...
echo.

rem ---- 1. Start Docker Compose ----
docker compose --env-file .env -f docker/docker-compose.yml up -d --build
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services.
    pause
    exit /b 1
)

rem ---- 2. Read Signal phone from .env ----
if exist .env (
    for /f "tokens=2 delims==" %%a in ('findstr /R "^SIGNAL_SERVICE_PHONE=" .env') do set SIGNAL_SERVICE_PHONE=%%a
)

rem ---- 3. Start bridge if phone set ----
if not "%SIGNAL_SERVICE_PHONE%"=="" (
    echo Launching Signal bridge...
    start "Signal Bridge" cmd /k "cd /d %cd% && set SIGNAL_SERVICE_PHONE=%SIGNAL_SERVICE_PHONE% && python src\backend\scripts\signal_bridge.py"
) else (
    echo No Signal phone configured. Bridge not started.
)

echo.
echo System started.
pause
endlocal