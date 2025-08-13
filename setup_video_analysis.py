#!/usr/bin/env python3
"""
Setup script for Cat Video Analysis
Installs required dependencies and creates folder structure
"""

import subprocess
import sys
import os


def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False


def create_folders():
    """Create the folder structure"""
    folders = [
        'extracted_audio',
        'audio_analysis_graphs',
        'input_videos',
        'video_analysis_results',
        'combined_analysis_results'
    ]

    print("📁 Creating folder structure...")
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"  Created: {folder}/")

    print("✅ Folder structure created!")


def main():
    print("🐱 CAT VIDEO ANALYSIS SETUP 🐱")
    print("=" * 40)

    # Install packages
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return

    # Create folders
    create_folders()

    print("\n✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Place your cat videos in the 'input_videos/' folder")
    print("2. Run: python3 video_analysis.py")
    print("\n🎬 Supported video formats: MP4, AVI, MOV, MKV, WMV")


if __name__ == "__main__":
    main()
