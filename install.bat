@echo off
setlocal EnableExtensions

echo ==========================================
echo  SignalShop - Installation automatique
echo ==========================================
echo.

rem Vérifier Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Docker n'est pas installe.
    echo Veuillez installer Docker Desktop depuis https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

rem Vérifier Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Git n'est pas installe.
    echo Veuillez installer Git depuis https://git-scm.com/downloads
    pause
    exit /b 1
)

rem Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe.
    echo Veuillez installer Python depuis https://www.python.org/downloads/
    echo Cochez "Add Python to PATH".
    pause
    exit /b 1
)

rem Télécharger le projet s'il n'existe pas
if not exist "src" (
    echo Téléchargement du dépôt SignalShop...
    git clone https://github.com/KorOfficiel/SignalShop.git temp_folder
    xcopy /E /I temp_folder .
    rmdir /S /Q temp_folder
)

rem Demander les informations
echo.
echo  Configuration de l'administrateur...
set /p ADMIN_EMAIL="Email administrateur [admin@example.com]: "
if "%ADMIN_EMAIL%"=="" set ADMIN_EMAIL=admin@example.com

set /p ADMIN_PASSWORD="Mot de passe administrateur [admin1234]: "
if "%ADMIN_PASSWORD%"=="" set ADMIN_PASSWORD=admin1234

set /p SIGNAL_SERVICE_PHONE="Numero de service Signal (laissez vide si pas encore configure): "

rem Créer .env
echo.
echo  Création du fichier .env...
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
    echo ADMIN_EMAIL=%ADMIN_EMAIL%
    echo ADMIN_PASSWORD=%ADMIN_PASSWORD%
) > .env

rem Lancer Docker Compose
echo.
echo  Démarrage des services Docker...
docker compose --env-file .env -f docker/docker-compose.yml up -d --build
if %errorlevel% neq 0 (
    echo [ERREUR] Echec du démarrage.
    pause
    exit /b 1
)

rem Initialiser la base
echo.
echo  Initialisation de la base de donnees...
timeout /t 10 /nobreak >nul
docker exec -it signalshop_backend python -m scripts.init_db
docker exec -it signalshop_backend python -m scripts.create_initial_user

rem Lancer le bridge si numéro fourni
if not "%SIGNAL_SERVICE_PHONE%"=="" (
    echo Démarrage du bridge Signal...
    start "Signal Bridge" cmd /k "cd /d %cd% && set SIGNAL_SERVICE_PHONE=%SIGNAL_SERVICE_PHONE% && python src\backend\scripts\signal_bridge.py"
) else (
    echo Aucun numéro Signal fourni. Bridge non démarré.
)

echo.
echo ==========================================
echo  Installation terminée !
echo  Dashboard : http://localhost:3000
echo  Email : %ADMIN_EMAIL%
echo  Mot de passe : %ADMIN_PASSWORD%
echo ==========================================
pause
endlocal