#!/usr/bin/env python3
"""
Weather Forecast App Quick Start Script
Automates setup and launches the application
"""

import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n[{description}]")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ {description} timed out")
        return False
    except Exception as e:
        print(f"✗ {description} error: {e}")
        return False

def check_python():
    """Check if Python is available"""
    print("Checking Python installation...")
    try:
        version = sys.version_info
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} found")
        return True
    except:
        print("✗ Python not found")
        return False

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    
    # Try pip first
    if not run_command("pip install -r requirements.txt", "Installing with pip"):
        # Try alternative methods
        print("Trying alternative installation methods...")
        
        methods = [
            "python -m pip install -r requirements.txt",
            "python -m pip install flask requests geopy python-dotenv flask-cors",
            "py -m pip install flask requests geopy python-dotenv flask-cors"
        ]
        
        for method in methods:
            if run_command(method, f"Trying: {method}"):
                return True
        
        print("✗ All installation methods failed")
        return False
    
    return True

def check_api_key():
    """Check if API key is configured"""
    print("Checking API key configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("✗ .env file not found")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_openweathermap_api_key_here" in content:
            print("⚠ API key not configured!")
            print("\nTo get your API key:")
            print("1. Visit https://openweathermap.org/api")
            print("2. Sign up for a free account")
            print("3. Generate an API key")
            print("4. Edit .env file and replace the placeholder")
            print("\nThe app will run but may show API errors without a valid key.")
            return False
        else:
            print("✓ API key configured")
            return True

def start_app():
    """Start the Flask application"""
    print("Starting Weather Forecast App...")
    print("\n" + "="*50)
    print("🌤️  Weather Forecast App is starting...")
    print("📍 Available at: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open("http://localhost:5000")
            print("🌐 Browser tab opened")
        except:
            print("Could not open browser automatically")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the Flask app
    try:
        import app
        app.app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"✗ App failed to start: {e}")

def main():
    """Main setup and run workflow"""
    print("🌤️  Weather Forecast App - Quick Start")
    print("="*50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print(f"Working directory: {script_dir}")
    
    # Step 1: Check Python
    if not check_python():
        input("Press Enter to exit...")
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n⚠ Dependencies installation failed.")
        print("Please install manually:")
        print("pip install flask requests geopy python-dotenv flask-cors")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Step 3: Check API key
    api_key_ok = check_api_key()
    
    # Step 4: Start the app
    print("\n" + "="*50)
    print("Setup complete! Starting application...")
    print("="*50)
    
    try:
        start_app()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
    
    print("\n🌟 Thank you for using Weather Forecast App!")

if __name__ == "__main__":
    main()
