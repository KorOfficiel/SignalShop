@echo off
cd /d %~dp0

REM Lire l'ancienne clé
for /f "tokens=2 delims==" %%a in ('findstr /R "^ENCRYPTION_KEY=" .env') do set OLD_KEY=%%a

REM Générer une nouvelle clé (met à jour .env)
python src\backend\scripts\rotate_key.py .env

REM Lire la nouvelle clé
for /f "tokens=2 delims==" %%a in ('findstr /R "^ENCRYPTION_KEY=" .env') do set NEW_KEY=%%a

REM Rechiffrer dans Docker
docker exec -e OLD_ENCRYPTION_KEY=%OLD_KEY% -e NEW_ENCRYPTION_KEY=%NEW_KEY% -it signalshop_backend python -m scripts.recrypt_ssh_keys

echo Rotation et rechiffrement terminés.
pause