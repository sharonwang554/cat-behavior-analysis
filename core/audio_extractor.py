#!/usr/bin/env python3
"""
Unified audio extraction module supporting multiple methods
"""

import os
import shutil
import subprocess
from typing import Optional
from abc import ABC, abstractmethod


class AudioExtractor(ABC):
    """Base class for audio extraction methods"""

    @abstractmethod
    def extract_audio(self, video_path: str, output_path: str) -> bool:
        """Extract audio from video file"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this extraction method is available"""
        pass


class MoviePyAudioExtractor(AudioExtractor):
    """Audio extraction using MoviePy"""

    def __init__(self):
        self._moviepy_available = None

    def is_available(self) -> bool:
        """Check if MoviePy is available"""
        if self._moviepy_available is None:
            try:
                from moviepy import VideoFileClip
                self._moviepy_available = True
            except ImportError:
                self._moviepy_available = False

        return self._moviepy_available

    def extract_audio(self, video_path: str, output_path: str) -> bool:
        """Extract audio using MoviePy"""
        if not self.is_available():
            return False

        try:
            from moviepy import VideoFileClip

            print(f"🎵 Extracting audio using MoviePy...")

            video = VideoFileClip(video_path)
            audio = video.audio

            if audio is None:
                print(f"❌ No audio track found in {video_path}")
                return False

            audio.write_audiofile(output_path, logger=None)
            audio.close()
            video.close()

            return True

        except Exception as e:
            print(f"❌ MoviePy extraction failed: {e}")
            return False


class FFmpegAudioExtractor(AudioExtractor):
    """Audio extraction using FFmpeg"""

    def is_available(self) -> bool:
        """Check if FFmpeg is available"""
        return shutil.which('ffmpeg') is not None

    def extract_audio(self, video_path: str, output_path: str) -> bool:
        """Extract audio using FFmpeg"""
        if not self.is_available():
            print("❌ FFmpeg not found. Please install FFmpeg to extract audio.")
            print("💡 Install FFmpeg: https://ffmpeg.org/download.html")
            return False

        try:
            print(f"🎵 Extracting audio using FFmpeg...")

            cmd = [
                'ffmpeg', '-i', video_path,
                '-vn', '-acodec', 'pcm_s16le',
                '-ar', '22050', '-ac', '1',
                output_path, '-y'
            ]

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True
            )

            if result.returncode == 0:
                return True
            else:
                print(f"❌ FFmpeg error: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ FFmpeg extraction failed: {e}")
            return False


class UnifiedAudioExtractor:
    """Unified audio extractor that tries multiple methods"""

    def __init__(self):
        self.extractors = [
            MoviePyAudioExtractor(),
            FFmpegAudioExtractor()
        ]

    def extract_audio(self, video_path: str, output_dir: str) -> Optional[str]:
        """
        Extract audio from video using the best available method

        Args:
            video_path: Path to input video file
            output_dir: Directory to save extracted audio

        Returns:
            Path to extracted audio file or None if extraction failed
        """
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_output = os.path.join(output_dir, f"{video_name}_audio.wav")

        print(f"🎵 Extracting audio from {video_path}...")

        # Try each extractor until one succeeds
        for extractor in self.extractors:
            if extractor.is_available():
                if extractor.extract_audio(video_path, audio_output):
                    print(f"✅ Audio extracted to: {audio_output}")
                    return audio_output
                else:
                    print(
                        f"⚠️ {extractor.__class__.__name__} failed, trying next method...")

        print("❌ All audio extraction methods failed")
        return None

    def get_available_methods(self) -> list:
        """Get list of available extraction methods"""
        return [extractor.__class__.__name__ for extractor in self.extractors
                if extractor.is_available()]
