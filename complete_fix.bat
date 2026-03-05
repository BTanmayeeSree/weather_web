@echo off
echo ========================================
echo Complete Weather App Fix
echo ========================================
echo.

echo [STEP 1] Fixing pip for Python 3.13...
echo.

REM Try to fix pip
C:\Python313\python.exe -m ensurepip --default-pip
if errorlevel 1 (
    echo Downloading pip installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'"
    C:\Python313\python.exe get-pip.py
    del get-pip.py
)

echo.
echo [STEP 2] Installing Flask only (minimal requirement)...
C:\Python313\python.exe -m pip install flask
if errorlevel 1 (
    echo ERROR: Cannot install Flask. Trying alternative...
    C:\Python313\python.exe -c "import sys; print('Python path:', sys.executable)"
    echo Please check your Python installation.
    pause
    exit /b 1
)

echo.
echo [STEP 3] Starting Simple Weather App...
echo.
echo ========================================
echo 🌤️  Weather App Starting...
echo 📍 Open: http://localhost:5000
echo 🎨 Features: Glass morphism UI, animations
echo 🔍 Try: London, New York, Tokyo, Paris, Sydney
echo ========================================
echo.

C:\Python313\python.exe simple_app.py

echo.
echo App stopped. Press any key to exit...
pause
