@echo off
setlocal

where docker >nul 2>&1
if errorlevel 1 (
  echo ERROR: 'docker' command not found.
  exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
  echo ERROR: Docker daemon is not available.
  exit /b 1
)

echo Building local-app image...
docker build -t local-app .
if errorlevel 1 exit /b 1

docker rm -f local-app-dev >nul 2>&1

echo Starting container at http://localhost:8000
docker run --rm --name local-app-dev -p 8000:8000 local-app
