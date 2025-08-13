#!/usr/bin/env python3
"""
Configuration file for Cat Behavior Analysis System
Sets up matplotlib backend and other system configurations
"""

import matplotlib
import os
import warnings
warnings.filterwarnings('ignore')

# Configure matplotlib to use non-interactive backend BEFORE any other imports
# Use non-interactive backend to prevent GUI threading issues
matplotlib.use('Agg')

# Set environment variables for better compatibility
os.environ['MPLBACKEND'] = 'Agg'
os.environ['DISPLAY'] = ''  # Disable display for headless operation

print("✅ Configured non-interactive matplotlib backend")
