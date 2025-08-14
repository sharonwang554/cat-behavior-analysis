from analysis import analyze_cat_meow, interpret_meow, print_analysis_results
import cv2
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from moviepy import VideoFileClip
import os
import glob
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Import functions from existing analysis.py


class CatVideoAnalyzer:
    def __init__(self):
        self.setup_directories()

    def setup_directories(self):
        """Create organized folder structure"""
        self.folders = {
            'audio': 'extracted_audio',
            'audio_graphs': 'audio_analysis_graphs',
            'videos': 'input_videos',
            'video_results': 'video_analysis_results',
            'combined_results': 'combined_analysis_results'
        }

        for folder in self.folders.values():
            os.makedirs(folder, exist_ok=True)

        print("📁 Created folder structure:")
        for name, path in self.folders.items():
            print(f"  {name}: {path}/")

    def extract_audio_from_video(self, video_path):
        """Extract audio from video file and save to audio folder"""
        try:
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            audio_output = os.path.join(
                self.folders['audio'], f"{video_name}_audio.wav")

            print(f"🎵 Extracting audio from {video_path}...")

            # Load video and extract audio
            video = VideoFileClip(video_path)
            audio = video.audio

            if audio is None:
                print(f"❌ No audio track found in {video_path}")
                return None

            # Save audio as WAV file
            audio.write_audiofile(audio_output, logger=None)

            # Clean up
            audio.close()
            video.close()

            print(f"✅ Audio extracted to: {audio_output}")
            return audio_output

        except Exception as e:
            print(f"❌ Error extracting audio from {video_path}: {e}")
            return None

    def analyze_video_frames(self, video_path):
        """Analyze cat body language and movement in video frames"""
        try:
            print(f"🎥 Analyzing video frames from {video_path}...")

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"❌ Could not open video: {video_path}")
                return None

            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps

            # Initialize analysis variables
            movement_data = []
            brightness_data = []
            activity_levels = []

            frame_num = 0
            prev_frame = None

            # Sample every 10th frame for efficiency
            sample_rate = 10

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_num % sample_rate == 0:
                    # Convert to grayscale for analysis
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Calculate brightness (average pixel intensity)
                    brightness = np.mean(gray)
                    brightness_data.append(brightness)

                    # Calculate movement (frame difference)
                    if prev_frame is not None:
                        diff = cv2.absdiff(prev_frame, gray)
                        movement = np.mean(diff)
                        movement_data.append(movement)

                        # Activity level based on movement threshold
                        activity = "High" if movement > 15 else "Medium" if movement > 5 else "Low"
                        activity_levels.append(activity)

                    prev_frame = gray.copy()

                frame_num += 1

            cap.release()

            # Calculate timestamps for sampled frames
            timestamps = [i * sample_rate /
                          fps for i in range(len(brightness_data))]

            visual_analysis = {
                'duration': duration,
                'fps': fps,
                'total_frames': frame_count,
                'sampled_frames': len(brightness_data),
                'timestamps': timestamps,
                'movement_data': movement_data,
                'brightness_data': brightness_data,
                'activity_levels': activity_levels,
                'avg_movement': np.mean(movement_data) if movement_data else 0,
                'avg_brightness': np.mean(brightness_data),
                'dominant_activity': max(set(activity_levels), key=activity_levels.count) if activity_levels else "Unknown"
            }

            print(
                f"✅ Video analysis complete. Duration: {duration:.1f}s, Activity: {visual_analysis['dominant_activity']}")
            return visual_analysis

        except Exception as e:
            print(f"❌ Error analyzing video frames: {e}")
            return None

    def create_visual_analysis_plots(self, visual_data, video_name):
        """Create visualization plots for video analysis"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
                2, 2, figsize=(15, 10))

            timestamps = visual_data['timestamps']

            # Movement over time
            ax1.plot(timestamps[1:],
                     visual_data['movement_data'], 'b-', linewidth=2)
            ax1.set_title('Movement Activity Over Time')
            ax1.set_xlabel('Time (seconds)')
            ax1.set_ylabel('Movement Intensity')
            ax1.grid(True, alpha=0.3)

            # Brightness over time
            ax2.plot(
                timestamps, visual_data['brightness_data'], 'g-', linewidth=2)
            ax2.set_title('Scene Brightness Over Time')
            ax2.set_xlabel('Time (seconds)')
            ax2.set_ylabel('Average Brightness')
            ax2.grid(True, alpha=0.3)

            # Activity level distribution
            activity_counts = {level: visual_data['activity_levels'].count(level)
                               for level in set(visual_data['activity_levels'])}
            ax3.bar(activity_counts.keys(), activity_counts.values(),
                    color=['red', 'orange', 'green'])
            ax3.set_title('Activity Level Distribution')
            ax3.set_ylabel('Number of Frames')

            # Movement histogram
            ax4.hist(visual_data['movement_data'],
                     bins=20, alpha=0.7, color='purple')
            ax4.set_title('Movement Intensity Distribution')
            ax4.set_xlabel('Movement Intensity')
            ax4.set_ylabel('Frequency')

            plt.tight_layout()

            # Save plot
            plot_path = os.path.join(
                self.folders['video_results'], f"{video_name}_visual_analysis.png")
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"📊 Visual analysis plot saved: {plot_path}")
            return plot_path

        except Exception as e:
            print(f"❌ Error creating visual plots: {e}")
            return None

    def correlate_audio_visual(self, audio_results, visual_data, video_name):
        """Correlate audio analysis with visual analysis"""
        try:
            # Create correlation analysis
            correlation = {
                'video_name': video_name,
                'timestamp': datetime.now().isoformat(),
                'audio_analysis': audio_results,
                'visual_analysis': {
                    'duration': visual_data['duration'],
                    'dominant_activity': visual_data['dominant_activity'],
                    'avg_movement': visual_data['avg_movement'],
                    'avg_brightness': visual_data['avg_brightness']
                },
                'combined_interpretation': self.interpret_combined_behavior(audio_results, visual_data)
            }

            return correlation

        except Exception as e:
            print(f"❌ Error correlating audio-visual data: {e}")
            return None

    def interpret_combined_behavior(self, audio_results, visual_data):
        """Interpret cat behavior based on both audio and visual cues"""
        interpretation = {
            'overall_mood': 'Unknown',
            'behavior_pattern': 'Unknown',
            'recommendations': [],
            'confidence': 'Low'
        }

        try:
            # Get audio characteristics
            audio_emotion = audio_results.get('emotional_state', 'Unknown')
            audio_urgency = audio_results.get('urgency_level', 'Unknown')
            audio_meaning = audio_results.get('primary_meaning', 'Unknown')

            # Get visual characteristics
            activity_level = visual_data['dominant_activity']
            avg_movement = visual_data['avg_movement']

            # Combined interpretation logic
            if audio_emotion == 'Seeking attention/affection':
                if activity_level == 'High':
                    interpretation['overall_mood'] = 'Playful and attention-seeking'
                    interpretation['behavior_pattern'] = 'Active communication'
                    interpretation['recommendations'].append(
                        'Engage in interactive play')
                elif activity_level == 'Low':
                    interpretation['overall_mood'] = 'Calm but wanting attention'
                    interpretation['behavior_pattern'] = 'Gentle request'
                    interpretation['recommendations'].append(
                        'Provide gentle petting or attention')

            elif audio_emotion == 'Distressed':
                if activity_level == 'High':
                    interpretation['overall_mood'] = 'Agitated and distressed'
                    interpretation['behavior_pattern'] = 'Stress response'
                    interpretation['recommendations'].extend([
                        'Check for sources of stress',
                        'Consider veterinary consultation',
                        'Provide calm environment'
                    ])
                else:
                    interpretation['overall_mood'] = 'Quietly distressed'
                    interpretation['behavior_pattern'] = 'Subdued distress'
                    interpretation['recommendations'].extend([
                        'Monitor closely',
                        'Check for illness signs'
                    ])

            elif audio_urgency == 'High':
                interpretation['overall_mood'] = 'Demanding and urgent'
                interpretation['behavior_pattern'] = 'High-priority communication'
                interpretation['recommendations'].extend([
                    'Address immediate needs (food, water, litter)',
                    'Check for any urgent issues'
                ])

            # Set confidence based on data quality
            if audio_results.get('confidence') == 'High' and len(visual_data['activity_levels']) > 10:
                interpretation['confidence'] = 'High'
            elif audio_results.get('confidence') in ['High', 'Medium']:
                interpretation['confidence'] = 'Medium'

            return interpretation

        except Exception as e:
            print(f"❌ Error in combined interpretation: {e}")
            return interpretation

    def save_combined_results(self, correlation_data):
        """Save combined analysis results to JSON file"""
        try:
            video_name = correlation_data['video_name']
            results_path = os.path.join(
                self.folders['combined_results'], f"{video_name}_combined_analysis.json")

            with open(results_path, 'w') as f:
                json.dump(correlation_data, f, indent=2, default=str)

            print(f"💾 Combined results saved: {results_path}")
            return results_path

        except Exception as e:
            print(f"❌ Error saving combined results: {e}")
            return None

    def print_combined_results(self, correlation_data):
        """Print comprehensive analysis results"""
        print("\n" + "🐱" * 20)
        print("COMPREHENSIVE CAT BEHAVIOR ANALYSIS")
        print("🐱" * 20)

        video_name = correlation_data['video_name']
        audio = correlation_data['audio_analysis']
        visual = correlation_data['visual_analysis']
        combined = correlation_data['combined_interpretation']

        print(f"\n📹 Video: {video_name}")
        print(f"⏱️  Duration: {visual['duration']:.1f} seconds")
        print(f"🎵 Audio Emotion: {audio.get('emotional_state', 'Unknown')}")
        print(f"📊 Visual Activity: {visual['dominant_activity']}")

        print(f"\n🧠 COMBINED INTERPRETATION:")
        print(f"Overall Mood: {combined['overall_mood']}")
        print(f"Behavior Pattern: {combined['behavior_pattern']}")
        print(f"Analysis Confidence: {combined['confidence']}")

        if combined['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in combined['recommendations']:
                print(f"• {rec}")

        print("\n" + "=" * 50)

    def analyze_video(self, video_path):
        """Complete analysis pipeline for a single video"""
        print(f"\n🎬 Starting comprehensive analysis of: {video_path}")
        print("=" * 60)

        video_name = os.path.splitext(os.path.basename(video_path))[0]

        # Step 1: Extract audio
        audio_path = self.extract_audio_from_video(video_path)
        if not audio_path:
            return None

        # Step 2: Analyze audio (using existing functions)
        try:
            print(f"🎵 Analyzing extracted audio...")
            audio_results = analyze_cat_meow(audio_path)

            # Move audio graph to correct folder
            old_graph = f"meow_analysis_{os.path.splitext(os.path.basename(audio_path))[0]}.png"
            if os.path.exists(old_graph):
                new_graph = os.path.join(
                    self.folders['audio_graphs'], old_graph)
                os.rename(old_graph, new_graph)
                print(f"📊 Audio analysis graph moved to: {new_graph}")

        except Exception as e:
            print(f"❌ Error in audio analysis: {e}")
            return None

        # Step 3: Analyze video frames
        visual_data = self.analyze_video_frames(video_path)
        if not visual_data:
            return None

        # Step 4: Create visual analysis plots
        self.create_visual_analysis_plots(visual_data, video_name)

        # Step 5: Correlate audio and visual
        correlation_data = self.correlate_audio_visual(
            audio_results, visual_data, video_name)
        if not correlation_data:
            return None

        # Step 6: Save and display results
        self.save_combined_results(correlation_data)
        self.print_combined_results(correlation_data)

        return correlation_data

    def analyze_all_videos(self):
        """Analyze all video files in the videos folder"""
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv',
                            '*.wmv', '*.MP4', '*.AVI', '*.MOV', '*.MKV', '*.WMV']
        video_files = []

        # Look for videos in the videos folder
        for ext in video_extensions:
            video_files.extend(
                glob.glob(os.path.join(self.folders['videos'], ext)))

        # Also check current directory for videos
        for ext in video_extensions:
            current_dir_videos = glob.glob(ext)
            for video in current_dir_videos:
                # Move to videos folder
                new_path = os.path.join(
                    self.folders['videos'], os.path.basename(video))
                if not os.path.exists(new_path):
                    os.rename(video, new_path)
                    print(f"📁 Moved {video} to {new_path}")
                video_files.append(new_path)

        if not video_files:
            print("❌ No video files found!")
            print(
                f"Please place video files in the '{self.folders['videos']}' folder")
            print("Supported formats: MP4, AVI, MOV, MKV, WMV")
            return

        print(f"\n🎬 Found {len(video_files)} video file(s) to analyze:")
        for video in video_files:
            print(f"  • {os.path.basename(video)}")

        # Analyze each video
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
        print(f"📁 Check the following folders for results:")
        print(f"  • Audio files: {self.folders['audio']}/")
        print(f"  • Audio graphs: {self.folders['audio_graphs']}/")
        print(f"  • Video analysis: {self.folders['video_results']}/")
        print(f"  • Combined results: {self.folders['combined_results']}/")


if __name__ == "__main__":
    print("🐱 CAT VIDEO BEHAVIOR ANALYZER 🐱")
    print("=" * 50)

    analyzer = CatVideoAnalyzer()
    analyzer.analyze_all_videos()
