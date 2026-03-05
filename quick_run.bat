@echo off
echo ========================================
echo Quick Weather App Run
echo ========================================
echo.

echo [1/2] Installing Flask only...
C:\Python313\python.exe -m pip install flask

echo.
echo [2/2] Starting Weather App...
echo.
echo ========================================
echo 🌤️  Weather App Starting...
echo 📍 Open: http://localhost:5000
echo 🎨 Glass morphism UI ready
echo 🔍 Try: London, New York, Tokyo, Paris, Sydney
echo ========================================
echo.

C:\Python313\python.exe simple_app.py

pause
