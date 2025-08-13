#!/bin/bash

# Cat Behavior Analysis Web Interface Startup Script
# This script activates the virtual environment and starts the web server

echo "🐱 Starting Cat Behavior Analysis Web Interface..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "cat_analysis_env" ]; then
    echo "❌ Virtual environment not found. Creating it now..."
    python3.11 -m venv cat_analysis_env
    echo "✅ Virtual environment created"
    
    echo "📦 Installing dependencies..."
    source cat_analysis_env/bin/activate
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Virtual environment found"
    source cat_analysis_env/bin/activate
fi

echo "🌐 Starting web server..."
echo "📱 Access the interface at: http://localhost:5002"
echo "=================================================="

python start_web_interface.py