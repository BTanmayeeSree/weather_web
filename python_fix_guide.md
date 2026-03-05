# 🔧 Python Installation Fix Guide

## Issue: "Python was not found; run without arguments to install from the Microsoft Store"

This is a common Windows issue. Here are the solutions:

## Solution 1: Use Python Launcher (Recommended)
Instead of `python`, use `py` command:
```cmd
py --version
py -m pip install -r requirements.txt
py app.py
```

## Solution 2: Fix Python Path
1. Open Command Prompt as Administrator
2. Run these commands to add Python to PATH:
```cmd
setx PATH "%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\Scripts"
setx PATH "%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311"
```

## Solution 3: Disable App Execution Alias
1. Go to Settings > Apps > Advanced app settings
2. Find "App execution aliases"
3. Turn OFF "Python" and "python.exe" aliases
4. Try `python` command again

## Solution 4: Install Python Properly
1. Download from https://python.org
2. During installation, CHECK "Add Python to PATH"
3. Restart Command Prompt

## Quick Test Commands:
```cmd
# Test Python launcher
py --version

# Test pip
py -m pip --version

# Install packages
py -m pip install flask requests geopy python-dotenv flask-cors

# Run app
py app.py
```
