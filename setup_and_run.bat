@echo off
echo ========================================
echo Weather Forecast App Setup & Run
echo ========================================
echo.

echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
echo Python found successfully!

echo.
echo [2/6] Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    echo Trying alternative installation method...
    python -m pip install flask requests geopy python-dotenv flask-cors
    if errorlevel 1 (
        echo ERROR: Installation failed. Please run manually:
        echo pip install flask requests geopy python-dotenv flask-cors
        pause
        exit /b 1
    )
)
echo Packages installed successfully!

echo.
echo [3/6] Checking API key configuration...
findstr "your_openweathermap_api_key_here" .env >nul
if not errorlevel 1 (
    echo WARNING: API key not configured!
    echo.
    echo Please follow these steps:
    echo 1. Go to https://openweathermap.org/api
    echo 2. Sign up for free account
    echo 3. Get your API key
    echo 4. Edit .env file and replace "your_openweathermap_api_key_here"
    echo.
    echo For now, the app will run but may show API errors.
    echo Press any key to continue anyway...
    pause >nul
)
echo API key check completed!

echo.
echo [4/6] Starting the Weather Forecast App...
echo.
echo ========================================
echo App will be available at: http://localhost:5000
echo ========================================
echo Press Ctrl+C to stop the server
echo.

python app.py

echo.
echo [5/6] App stopped. Cleaning up...
echo.

echo [6/6] Setup complete!
echo Thank you for using Weather Forecast App!
echo.
pause
