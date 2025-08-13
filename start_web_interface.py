#!/usr/bin/env python3
"""
Startup script for Cat Behavior Analysis Web Interface
"""

import os
import sys
import subprocess


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask not found. Installing...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "flask", "werkzeug"])
        print("✅ Flask installed successfully")


def main():
    print("🐱 Cat Behavior Analysis Web Interface")
    print("=" * 50)

    # Check dependencies
    check_dependencies()

    # Create necessary directories
    directories = ['input_videos', 'downloads', 'templates']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("\n📁 Directory structure ready")
    print("📹 Place your cat videos in the 'input_videos/' folder")
    print("🌐 Starting web server...")
    print("📱 Access the interface at: http://localhost:5002")
    print("\n" + "=" * 50)

    # Start the web application
    try:
        from web_app import app
        app.run(debug=False, host='0.0.0.0', port=5002)
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped")
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        print("Make sure all dependencies are installed and try again")


if __name__ == "__main__":
    main()
