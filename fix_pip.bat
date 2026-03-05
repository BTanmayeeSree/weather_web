@echo off
echo ========================================
echo Fixing pip for Python 3.13
echo ========================================
echo.

echo [1/4] Checking Python installation...
C:\Python313\python.exe --version
if errorlevel 1 (
    echo ERROR: Python 3.13 not found at C:\Python313\python.exe
    echo Please check your Python installation path
    pause
    exit /b 1
)

echo.
echo [2/4] Installing pip...
C:\Python313\python.exe -m ensurepip --default-pip
if errorlevel 1 (
    echo Trying alternative pip installation...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    C:\Python313\python.exe get-pip.py
    del get-pip.py
)

echo.
echo [3/4] Upgrading pip...
C:\Python313\python.exe -m pip install --upgrade pip

echo.
echo [4/4] Installing required packages...
C:\Python313\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo Installing packages individually...
    C:\Python313\python.exe -m pip install flask
    C:\Python313\python.exe -m pip install requests
    C:\Python313\python.exe -m pip install geopy
    C:\Python313\python.exe -m pip install python-dotenv
    C:\Python313\python.exe -m pip install flask-cors
)

echo.
echo pip installation and package setup complete!
echo Now you can run: C:\Python313\python.exe app.py
pause
