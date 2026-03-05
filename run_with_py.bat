@echo off
echo ========================================
echo Weather Forecast App - Python Fix
echo ========================================
echo.

echo Using Python launcher instead of python command...
echo.

echo [1/4] Checking Python launcher...
py --version
if errorlevel 1 (
    echo ERROR: Python launcher not found
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo Trying alternative installation...
    py -m pip install flask requests geopy python-dotenv flask-cors
)

echo.
echo [3/4] Starting Weather App...
echo App will be available at: http://localhost:5000
echo Press Ctrl+C to stop
echo.

py app.py

echo.
echo [4/4] App stopped.
pause
