@echo off
echo ========================================
echo Modern Weather App Launcher
echo ========================================
echo.

echo [1/2] Installing Flask...
C:\Python313\python.exe -m pip install flask

echo.
echo [2/2] Starting Modern Weather App...
echo.
echo ========================================
echo 🌤️  Modern Weather App Starting...
echo 📍 Open: http://localhost:5000
echo 🎨 Features: Blue sky UI, Location pin, Sun icon
echo 📊 AQI Circle, Pollen card, Hourly & Daily forecasts
echo 📱 Mobile-optimized, Search functionality
echo 🔍 Try: Seethariguda, London, New York
echo ========================================
echo.

C:\Python313\python.exe modern_weather_app.py

pause
