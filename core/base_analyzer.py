#!/usr/bin/env python3
"""
Base analyzer class with shared functionality for all cat behavior analyzers
"""

import os
import shutil
from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from datetime import datetime


class AnalyzerConfig:
    """Centralized configuration for all analyzers"""

    # Folder structure - single source of truth
    FOLDERS = {
        'audio': 'extracted_audio',
        'audio_graphs': 'audio_analysis_graphs',
        'videos': 'input_videos',
        'video_results': 'video_analysis_results',
        'combined_results': 'combined_analysis_results',
        'ml_results': 'ml_analysis_results',
        'models': 'ml_models',
        'features': 'extracted_features',
        'training_data': 'training_data',
        'downloads': 'downloads'
    }

    # Video file extensions
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']

    # Audio processing settings
    AUDIO_SAMPLE_RATE = 22050
    AUDIO_CHANNELS = 1

    # Video processing settings
    VIDEO_SAMPLE_RATE = 10  # Sample every 10th frame
    MAX_FRAMES_TO_PROCESS = 300  # Limit for performance


class BaseAnalyzer(ABC):
    """Base class for all cat behavior analyzers"""

    def __init__(self, folders_to_create: Optional[List[str]] = None):
        """
        Initialize analyzer with specified folders

        Args:
            folders_to_create: List of folder keys to create. If None, creates all folders.
        """
        self.config = AnalyzerConfig()
        self.folders = self.config.FOLDERS

        # Create only specified folders or all if none specified
        folders_to_setup = folders_to_create or list(self.folders.keys())
        self.setup_directories(folders_to_setup)

    def setup_directories(self, folder_keys: List[str]) -> None:
        """Create organized folder structure"""
        print("📁 Setting up directory structure...")

        for key in folder_keys:
            if key in self.folders:
                folder_path = self.folders[key]
                os.makedirs(folder_path, exist_ok=True)
                print(f"  {key}: {folder_path}/")

        print("✅ Directory structure ready!")

    def cleanup_results(self, folder_keys: Optional[List[str]] = None) -> None:
        """Clean up previous analysis results"""
        folders_to_clean = folder_keys or [
            'audio', 'audio_graphs', 'video_results', 'combined_results'
        ]

        print("🧹 Cleaning up previous results...")
        for key in folders_to_clean:
            if key in self.folders:
                folder_path = self.folders[key]
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                    os.makedirs(folder_path, exist_ok=True)
                    print(f"  Cleaned: {folder_path}/")

        print("✅ Cleanup complete!")

    def get_video_files(self) -> List[str]:
        """Get all video files from the input directory"""
        video_files = []
        input_dir = self.folders['videos']

        for ext in self.config.VIDEO_EXTENSIONS:
            # Check both lowercase and uppercase extensions
            for case_ext in [ext.lower(), ext.upper()]:
                pattern = os.path.join(input_dir, f'*{case_ext}')
                video_files.extend([f for f in os.listdir(input_dir)
                                    if f.lower().endswith(ext.lower())])

        return [os.path.join(input_dir, f) for f in set(video_files)]

    def get_video_name(self, video_path: str) -> str:
        """Extract clean video name from path"""
        return os.path.splitext(os.path.basename(video_path))[0]

    def save_results_json(self, data: dict, filename: str, folder_key: str = 'combined_results') -> Optional[str]:
        """Save analysis results to JSON file"""
        try:
            results_path = os.path.join(self.folders[folder_key], filename)

            with open(results_path, 'w') as f:
                import json
                json.dump(data, f, indent=2, default=str)

            print(f"💾 Results saved: {results_path}")
            return results_path

        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return None

    @abstractmethod
    def analyze_video(self, video_path: str) -> Optional[dict]:
        """Analyze a single video - must be implemented by subclasses"""
        pass

    def analyze_all_videos(self) -> List[dict]:
        """Analyze all videos in the input directory"""
        video_files = self.get_video_files()

        if not video_files:
            print("❌ No video files found!")
            print(
                f"Please place video files in the '{self.folders['videos']}' folder")
            print(
                f"Supported formats: {', '.join(self.config.VIDEO_EXTENSIONS)}")
            return []

        print(f"\n🎬 Found {len(video_files)} video file(s) to analyze:")
        for video in video_files:
            print(f"  • {os.path.basename(video)}")

        results = []
        for i, video_path in enumerate(video_files, 1):
            print(f"\n{'='*60}")
            print(f"PROCESSING VIDEO {i}/{len(video_files)}")
            print(f"{'='*60}")

            result = self.analyze_video(video_path)
            if result:
                results.append(result)

        print(
            f"\n✅ Analysis complete! Processed {len(results)} videos successfully.")
        return results
