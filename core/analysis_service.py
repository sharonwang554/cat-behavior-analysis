#!/usr/bin/env python3
"""
Analysis service layer for web interface
Separates business logic from web presentation
"""

import os
import json
import glob
import shutil
import zipfile
from datetime import datetime
from typing import Dict, List, Optional, Any
from simple_video_analysis import SimpleCatVideoAnalyzer

# Try to import enhanced analyzer
try:
    from enhanced_video_analysis import EnhancedCatVideoAnalyzer, MOVIEPY_AVAILABLE
    ML_AVAILABLE = MOVIEPY_AVAILABLE
except ImportError:
    EnhancedCatVideoAnalyzer = None
    ML_AVAILABLE = False


class AnalysisService:
    """Service layer for cat behavior analysis operations"""

    def __init__(self):
        self.analyzer = SimpleCatVideoAnalyzer()
        self.enhanced_analyzer = EnhancedCatVideoAnalyzer() if ML_AVAILABLE else None
        self.results_cache = {}
        self.use_ml = ML_AVAILABLE

    def get_status(self) -> Dict[str, Any]:
        """Get current analysis status"""
        video_files = self._get_video_files()
        results = self.load_results()

        return {
            'videos_found': len(video_files),
            'results_available': len(results),
            'video_files': [os.path.basename(f) for f in video_files],
            'ml_available': ML_AVAILABLE,
            'current_mode': 'Enhanced ML' if self.use_ml else 'Traditional'
        }

    def cleanup_previous_results(self) -> None:
        """Remove all previous analysis results"""
        self.analyzer.cleanup_results()
        self.results_cache = {}

    def run_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis and return results"""
        try:
            self.cleanup_previous_results()

            print("🚀 Running Combined Analysis (Traditional + ML)...")

            # Always run traditional analysis first
            print("📊 Step 1: Running traditional analysis...")
            self.analyzer.analyze_all_videos()

            # Run enhanced ML analysis if available
            if self.enhanced_analyzer:
                print("🧠 Step 2: Running enhanced ML analysis...")
                video_files = self._get_video_files()

                for video_path in video_files:
                    result = self.enhanced_analyzer.analyze_video(video_path)
                    if result is None:
                        print("⚠️ Enhanced analysis failed for", video_path)
            else:
                print(
                    "💡 ML analysis not available - install MoviePy for enhanced features")

            # Load and cache results
            self.load_results()

            return {
                'success': True,
                'message': f'Analysis complete! Processed {len(self.results_cache)} videos.',
                'results_count': len(self.results_cache)
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Analysis failed: {str(e)}'
            }

    def load_results(self) -> Dict[str, Any]:
        """Load analysis results from JSON files"""
        self.results_cache = {}

        json_files = glob.glob('combined_analysis_results/*.json')

        # Separate regular and enhanced analysis files
        regular_files = [f for f in json_files if 'enhanced_analysis' not in f]
        enhanced_files = [f for f in json_files if 'enhanced_analysis' in f]

        # Load regular files first
        for json_file in regular_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    video_name = data.get('video_name', os.path.splitext(
                        os.path.basename(json_file))[0])
                    self.results_cache[video_name] = data
            except Exception as e:
                print(f"Error loading {json_file}: {e}")

        # Load enhanced files if no regular file exists for that video
        for json_file in enhanced_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    video_name = data.get('video_name', os.path.splitext(
                        os.path.basename(json_file))[0])

                    if video_name not in self.results_cache:
                        converted_data = self._convert_enhanced_to_regular_format(
                            data)
                        self.results_cache[video_name] = converted_data
            except Exception as e:
                print(f"Error loading {json_file}: {e}")

        return self.results_cache

    def create_download_package(self) -> str:
        """Create a ZIP file with all analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"cat_analysis_results_{timestamp}.zip"
        zip_path = os.path.join('downloads', zip_filename)

        # Create downloads directory
        os.makedirs('downloads', exist_ok=True)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            folders_to_include = [
                'extracted_audio',
                'audio_analysis_graphs',
                'video_analysis_results',
                'combined_analysis_results'
            ]

            for folder in folders_to_include:
                if os.path.exists(folder):
                    for root, dirs, files in os.walk(folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path)
                            zipf.write(file_path, arcname)

        return zip_path

    def generate_analysis_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive text report"""
        report_lines = []

        # Header
        report_lines.extend([
            "🐱 CAT BEHAVIOR ANALYSIS REPORT",
            "=" * 50,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Videos Analyzed: {len(results)}",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 20
        ])

        # Overall statistics
        if results:
            emotions = [r.get('audio_analysis', {}).get('emotional_state', 'Unknown')
                        for r in results.values()]
            activities = [r.get('visual_analysis', {}).get('dominant_activity', 'Unknown')
                          for r in results.values()]
            urgencies = [r.get('audio_analysis', {}).get('urgency_level', 'Unknown')
                         for r in results.values()]

            # Count occurrences
            emotion_counts = {}
            activity_counts = {}
            urgency_counts = {}

            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            for activity in activities:
                activity_counts[activity] = activity_counts.get(
                    activity, 0) + 1
            for urgency in urgencies:
                urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1

            # Most common patterns
            most_common_emotion = max(
                emotion_counts, key=emotion_counts.get) if emotion_counts else "Unknown"
            most_common_activity = max(
                activity_counts, key=activity_counts.get) if activity_counts else "Unknown"
            most_common_urgency = max(
                urgency_counts, key=urgency_counts.get) if urgency_counts else "Unknown"

            report_lines.extend([
                f"Most Common Emotional State: {most_common_emotion} ({emotion_counts.get(most_common_emotion, 0)} videos)",
                f"Most Common Activity Level: {most_common_activity} ({activity_counts.get(most_common_activity, 0)} videos)",
                f"Most Common Urgency Level: {most_common_urgency} ({urgency_counts.get(most_common_urgency, 0)} videos)",
                ""
            ])

        # Individual video analysis
        report_lines.extend([
            "DETAILED VIDEO ANALYSIS",
            "-" * 25,
            ""
        ])

        for video_name, result in results.items():
            audio = result.get('audio_analysis', {})
            visual = result.get('visual_analysis', {})
            combined = result.get('combined_interpretation', {})

            report_lines.extend([
                f"📹 VIDEO: {video_name}",
                f"   Duration: {visual.get('duration', 'Unknown'):.1f} seconds" if isinstance(visual.get(
                    'duration'), (int, float)) else f"   Duration: {visual.get('duration', 'Unknown')}",
                f"   Timestamp: {result.get('timestamp', 'Unknown')}",
                "",
                "   🎵 AUDIO ANALYSIS:",
                f"      Emotional State: {audio.get('emotional_state', 'Unknown')}",
                f"      Primary Meaning: {audio.get('primary_meaning', 'Unknown')}",
                f"      Urgency Level: {audio.get('urgency_level', 'Unknown')}",
                f"      Confidence: {audio.get('confidence', 'Unknown')}",
                "",
                "   🎥 VIDEO ANALYSIS:",
                f"      Activity Level: {visual.get('dominant_activity', 'Unknown')}",
                f"      Average Movement: {visual.get('avg_movement', 'Unknown')}",
                f"      Average Brightness: {visual.get('avg_brightness', 'Unknown')}",
                ""
            ])

            if combined:
                report_lines.extend([
                    "   🧠 COMBINED INTERPRETATION:",
                    f"      Overall Mood: {combined.get('overall_mood', 'Unknown')}",
                    f"      Behavior Pattern: {combined.get('behavior_pattern', 'Unknown')}",
                    f"      Analysis Confidence: {combined.get('confidence', 'Unknown')}",
                    ""
                ])

                if combined.get('recommendations'):
                    report_lines.append("   💡 RECOMMENDATIONS:")
                    for rec in combined.get('recommendations', []):
                        report_lines.append(f"      • {rec}")
                    report_lines.append("")

            report_lines.append("-" * 50)
            report_lines.append("")

        # Footer
        report_lines.extend([
            "ANALYSIS METHODOLOGY",
            "-" * 20,
            "",
            "This analysis uses advanced AI techniques including:",
            "• Audio signal processing to isolate and analyze cat vocalizations",
            "• Computer vision to track movement patterns and activity levels",
            "• Machine learning algorithms to interpret behavioral patterns",
            "• Correlation analysis to combine audio and visual cues",
            "",
            "IMPORTANT NOTES:",
            "• This analysis is for informational purposes only",
            "• Individual cats may have unique vocal and behavioral characteristics",
            "• Consult with a veterinarian for any health or behavioral concerns",
            "• Results should be considered alongside direct observation",
            "",
            "Generated by Cat Behavior Analysis System",
            ""
        ])

        return "\n".join(report_lines)

    def _get_video_files(self) -> List[str]:
        """Get all video files from input directory"""
        return self.analyzer.get_video_files()

    def _convert_enhanced_to_regular_format(self, enhanced_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert enhanced analysis format to regular format for template compatibility"""
        try:
            # Extract traditional analysis data
            traditional = enhanced_data.get('traditional_analysis', {})
            enhanced_interpretation = enhanced_data.get(
                'enhanced_interpretation', {})
            ml_analysis = enhanced_data.get('ml_analysis', {})

            # Extract activity level from enhanced interpretation or ML analysis
            activity_level = enhanced_interpretation.get(
                'activity_level', 'Unknown')

            # Normalize case - convert to proper case
            if activity_level and activity_level != 'Unknown':
                activity_level = activity_level.capitalize()

            # If activity level is still unknown, try to derive from ML analysis
            if activity_level == 'Unknown' or not activity_level:
                ml_prediction = ml_analysis.get('ml_prediction', '').lower()
                if 'excited' in ml_prediction or 'active' in ml_prediction:
                    activity_level = 'High'
                elif 'calm' in ml_prediction or 'relaxed' in ml_prediction:
                    activity_level = 'Low'
                else:
                    # Check feature analysis for activity indicators
                    feature_analysis = ml_analysis.get('feature_analysis', [])
                    for feature in feature_analysis:
                        if 'high activity' in feature.lower():
                            activity_level = 'High'
                            break
                        elif 'low activity' in feature.lower():
                            activity_level = 'Low'
                            break
                        elif 'medium activity' in feature.lower():
                            activity_level = 'Medium'
                            break

                    # If still unknown, default based on overall behavior
                    if activity_level == 'Unknown':
                        overall_behavior = enhanced_interpretation.get(
                            'overall_behavior', '').lower()
                        if 'highly_active' in overall_behavior or 'active' in overall_behavior:
                            activity_level = 'High'
                        elif 'calm' in overall_behavior or 'relaxed' in overall_behavior:
                            activity_level = 'Low'
                        else:
                            activity_level = 'Medium'  # Default fallback

            # Create a regular format structure
            regular_data = {
                'video_name': enhanced_data.get('video_name', 'unknown'),
                'timestamp': enhanced_data.get('timestamp', ''),
                'audio_analysis': traditional,
                'visual_analysis': {
                    'duration': 0,
                    'dominant_activity': activity_level,
                    'avg_movement': 0.5,  # Default reasonable value
                    'avg_brightness': 128  # Default reasonable value
                },
                'combined_interpretation': {
                    'overall_mood': enhanced_interpretation.get('overall_behavior', 'Unknown'),
                    'behavior_pattern': enhanced_interpretation.get('behavioral_complexity', 'Unknown'),
                    'confidence': enhanced_data.get('confidence_assessment', {}).get('recommendation', 'Unknown'),
                    'recommendations': enhanced_data.get('comprehensive_recommendations', [])
                }
            }

            # Try to extract duration from acoustic metrics if available
            if traditional and 'acoustic_metrics' in traditional:
                duration_ms = traditional['acoustic_metrics'].get(
                    'duration_ms', 0)
                # Convert to seconds
                regular_data['visual_analysis']['duration'] = duration_ms / 1000.0

            return regular_data

        except Exception as e:
            print(f"Error converting enhanced format: {e}")
            # Return a minimal structure if conversion fails
            return {
                'video_name': enhanced_data.get('video_name', 'unknown'),
                'timestamp': enhanced_data.get('timestamp', ''),
                'audio_analysis': {'primary_meaning': 'Analysis unavailable', 'emotional_state': 'Unknown', 'urgency_level': 'Unknown', 'confidence': 'Low'},
                'visual_analysis': {'duration': 0, 'dominant_activity': 'Medium', 'avg_movement': 0, 'avg_brightness': 0},
                'combined_interpretation': {'overall_mood': 'Unknown', 'behavior_pattern': 'Unknown', 'confidence': 'Low', 'recommendations': []}
            }
