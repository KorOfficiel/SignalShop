@echo off
setlocal EnableExtensions

rem ==================================================
rem  SignalShop Installation Script
rem ==================================================

echo.
echo  *************************************************
echo  *             SIGNALSHOP INSTALLER              *
echo  *************************************************
echo.

rem ---- 1. Check Docker ----
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed.
    echo Please download and install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

rem ---- 2. Check Git ----
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed.
    echo Please download and install Git from:
    echo https://git-scm.com/downloads
    pause
    exit /b 1
)

rem ---- 3. Check Python ----
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed.
    echo Please download and install Python from:
    echo https://www.python.org/downloads/
    echo During installation, check "Add Python to PATH".
    pause
    exit /b 1
)

echo.
echo  [1/5] Configuration...
echo.

rem ---- 4. Admin email ----
set /p ADMIN_EMAIL="Enter admin email [admin@example.com]: "
if "%ADMIN_EMAIL%"=="" set ADMIN_EMAIL=admin@example.com

rem ---- 5. Admin password ----
set /p ADMIN_PASSWORD="Enter admin password [admin1234]: "
if "%ADMIN_PASSWORD%"=="" set ADMIN_PASSWORD=admin1234

rem ---- 6. Signal service phone ----
set /p SIGNAL_SERVICE_PHONE="Enter Signal service phone (leave empty if not ready): "

rem ---- 7. Create .env file ----
echo.
echo  [2/5] Creating .env file...
(
    echo POSTGRES_USER=signaluser
    echo POSTGRES_PASSWORD=change_this_strong_password
    echo POSTGRES_DB=signal_shop
    echo DATABASE_URL=postgresql://signaluser:change_this_strong_password@db:5432/signal_shop
    echo REDIS_URL=redis://redis:6379/0
    echo SECRET_KEY=change_this_secret_key
    echo BACKEND_PORT=8000
    echo FRONTEND_PORT=3000
    echo SIGNAL_SERVICE_PHONE=%SIGNAL_SERVICE_PHONE%
    echo SIGNAL_PRO_PHONE=+33...
    echo SIGNAL_CLI_VERSION=0.12.0
    echo ADMIN_EMAIL=%ADMIN_EMAIL%
    echo ADMIN_PASSWORD=%ADMIN_PASSWORD%
) > .env

rem ---- 8. Start Docker Compose ----
echo.
echo  [3/5] Building and starting services...
echo.
docker compose --env-file .env -f docker/docker-compose.yml up -d --build
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start Docker services.
    pause
    exit /b 1
)

rem ---- 9. Wait for DB ----
echo.
echo  [4/5] Waiting for database...
timeout /t 10 /nobreak >nul

rem ---- 10. Initialize DB and create admin ----
echo.
echo  [5/5] Initializing database...
docker exec -it signalshop_backend python -m scripts.init_db
docker exec -it signalshop_backend python -m scripts.create_initial_user
if %errorlevel% neq 0 (
    echo [WARNING] Database initialization encountered an issue. Check logs.
)

rem ---- 11. Start Signal bridge if phone provided ----
if not "%SIGNAL_SERVICE_PHONE%"=="" (
    echo.
    echo  Launching Signal bridge...
    start "Signal Bridge" cmd /k "cd /d %cd% && set SIGNAL_SERVICE_PHONE=%SIGNAL_SERVICE_PHONE% && python src\backend\scripts\signal_bridge.py"
) else (
    echo.
    echo  Signal bridge not started: no phone number provided.
)

echo.
echo  *************************************************
echo  *       Installation completed successfully!    *
echo  *************************************************
echo.
echo  Dashboard   : http://localhost:3000
echo  Admin email : %ADMIN_EMAIL%
echo  Admin pass  : %ADMIN_PASSWORD%
echo.
echo  Press any key to exit...
pause >nul
endlocal