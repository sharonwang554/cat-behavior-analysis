#!/usr/bin/env python3
"""
Cat Behavior Analysis Web Interface
Displays analysis results on a webpage with download options
"""

# Import configuration first to set matplotlib backend
from config import *

from flask import Flask, render_template, send_file, request, jsonify, redirect, url_for, flash
import os
import json
import shutil
import zipfile
from datetime import datetime
import glob
from werkzeug.utils import secure_filename
from simple_video_analysis import SimpleCatVideoAnalyzer

# Try to import enhanced analyzer, fall back to simple if not available
try:
    from enhanced_video_analysis import EnhancedCatVideoAnalyzer, MOVIEPY_AVAILABLE
    ML_AVAILABLE = MOVIEPY_AVAILABLE  # ML is only available if MoviePy is available
    if not MOVIEPY_AVAILABLE:
        print("⚠️ Enhanced ML analysis disabled: MoviePy not available")
        print("📝 Install MoviePy with: pip install moviepy")
        print("📝 Falling back to traditional analysis only")
except ImportError as e:
    print(f"⚠️ Enhanced ML analysis not available: {e}")
    print("📝 Falling back to traditional analysis only")
    EnhancedCatVideoAnalyzer = None
    ML_AVAILABLE = False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'input_videos'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.secret_key = 'cat_behavior_analysis_secret_key_2024'

# Allowed video file extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv',
                      'wmv', 'MP4', 'AVI', 'MOV', 'MKV', 'WMV'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class WebCatAnalyzer:
    def __init__(self):
        self.analyzer = SimpleCatVideoAnalyzer()
        self.enhanced_analyzer = EnhancedCatVideoAnalyzer() if ML_AVAILABLE else None
        self.results_cache = {}
        self.use_ml = ML_AVAILABLE  # Enable ML analysis only if available

    def cleanup_previous_results(self):
        """Remove all previous analysis results before new run"""
        folders_to_clean = [
            'extracted_audio',
            'audio_analysis_graphs',
            'video_analysis_results',
            'combined_analysis_results'
        ]

        print("🧹 Cleaning up previous analysis results...")
        for folder in folders_to_clean:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                os.makedirs(folder, exist_ok=True)
                print(f"  Cleaned: {folder}/")

        self.results_cache = {}
        print("✅ Cleanup complete!")

    def run_analysis(self):
        """Run the analysis and cache results"""
        self.cleanup_previous_results()

        if self.use_ml and self.enhanced_analyzer:
            # Run enhanced ML analysis
            print("🧠 Running enhanced ML analysis...")
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
            video_files = []

            for ext in video_extensions:
                for case_ext in [ext.lower(), ext.upper()]:
                    video_files.extend(glob.glob(f'input_videos/*{case_ext}'))

            for video_path in video_files:
                result = self.enhanced_analyzer.analyze_video(video_path)
                if result is None:
                    print(
                        "⚠️ Enhanced analysis failed, falling back to traditional analysis")
                    self.analyzer.analyze_all_videos()
                    break
        elif self.use_ml and not self.enhanced_analyzer:
            # ML requested but not available
            print("⚠️ ML analysis requested but not available")
            print("💡 Install MoviePy with: pip install moviepy")
            print("📊 Falling back to traditional analysis...")
            self.analyzer.analyze_all_videos()
        else:
            # Run traditional analysis
            print("📊 Running traditional analysis...")
            self.analyzer.analyze_all_videos()

        # Cache the results
        self.load_results()

        return self.results_cache

    def load_results(self):
        """Load analysis results from JSON files"""
        self.results_cache = {}

        json_files = glob.glob('combined_analysis_results/*.json')

        # Separate regular and enhanced analysis files
        regular_files = [f for f in json_files if 'enhanced_analysis' not in f]
        enhanced_files = [f for f in json_files if 'enhanced_analysis' in f]

        # Load regular files first (they have the structure templates expect)
        for json_file in regular_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    video_name = data.get('video_name', os.path.splitext(
                        os.path.basename(json_file))[0])
                    self.results_cache[video_name] = data
            except Exception as e:
                print(f"Error loading {json_file}: {e}")

        # Only load enhanced files if no regular file exists for that video
        for json_file in enhanced_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    video_name = data.get('video_name', os.path.splitext(
                        os.path.basename(json_file))[0])

                    # Only use enhanced analysis if no regular analysis exists
                    if video_name not in self.results_cache:
                        # Convert enhanced analysis structure to regular structure for template compatibility
                        converted_data = self.convert_enhanced_to_regular_format(
                            data)
                        self.results_cache[video_name] = converted_data
            except Exception as e:
                print(f"Error loading {json_file}: {e}")

        return self.results_cache

    def convert_enhanced_to_regular_format(self, enhanced_data):
        """Convert enhanced analysis format to regular format for template compatibility"""
        try:
            # Extract traditional analysis data
            traditional = enhanced_data.get('traditional_analysis', {})

            # Create a regular format structure
            regular_data = {
                'video_name': enhanced_data.get('video_name', 'unknown'),
                'timestamp': enhanced_data.get('timestamp', ''),
                'audio_analysis': traditional,
                'visual_analysis': {
                    'duration': 0,
                    'dominant_activity': 'Unknown',
                    'avg_movement': 0,
                    'avg_brightness': 0
                },
                'combined_interpretation': {
                    'overall_mood': enhanced_data.get('enhanced_interpretation', {}).get('overall_behavior', 'Unknown'),
                    'behavior_pattern': enhanced_data.get('enhanced_interpretation', {}).get('behavioral_complexity', 'Unknown'),
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
                'visual_analysis': {'duration': 0, 'dominant_activity': 'Unknown', 'avg_movement': 0, 'avg_brightness': 0},
                'combined_interpretation': {'overall_mood': 'Unknown', 'behavior_pattern': 'Unknown', 'confidence': 'Low', 'recommendations': []}
            }

    def create_download_package(self):
        """Create a ZIP file with all analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"cat_analysis_results_{timestamp}.zip"
        zip_path = os.path.join('downloads', zip_filename)

        # Create downloads directory
        os.makedirs('downloads', exist_ok=True)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all analysis files
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

    def generate_analysis_report(self, results):
        """Generate a comprehensive text report of all analysis results"""
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
            emotions = [r.get('audio_analysis', {}).get(
                'emotional_state', 'Unknown') for r in results.values()]
            activities = [r.get('visual_analysis', {}).get(
                'dominant_activity', 'Unknown') for r in results.values()]
            urgencies = [r.get('audio_analysis', {}).get(
                'urgency_level', 'Unknown') for r in results.values()]

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

            # Overall recommendations
            report_lines.extend([
                "OVERALL BEHAVIORAL INSIGHTS",
                "-" * 30,
                ""
            ])

            if most_common_emotion == "Distressed":
                report_lines.append(
                    "⚠️  ATTENTION: Multiple videos show signs of distress. Consider:")
                report_lines.extend([
                    "   • Checking for environmental stressors",
                    "   • Ensuring adequate food, water, and comfort",
                    "   • Consulting with a veterinarian if distress persists",
                    ""
                ])
            elif most_common_emotion == "Content":
                report_lines.extend([
                    "✅ POSITIVE: Your cat appears generally content and comfortable.",
                    "   Continue current care routine.",
                    ""
                ])

            if most_common_urgency == "High":
                report_lines.extend([
                    "🔔 HIGH URGENCY DETECTED: Your cat frequently exhibits urgent vocalizations.",
                    "   This may indicate:",
                    "   • Need for immediate attention (food, water, litter box)",
                    "   • Medical concerns requiring veterinary evaluation",
                    "   • Anxiety or stress-related behaviors",
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

            # Add details if available
            if audio.get('details'):
                report_lines.append("   📋 DETAILED OBSERVATIONS:")
                for detail in audio.get('details', []):
                    report_lines.append(f"      • {detail}")
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
            "https://github.com/sharonwang554/cat-behavior-analysis",
            ""
        ])

        return "\n".join(report_lines)


# Initialize the analyzer
web_analyzer = WebCatAnalyzer()


@app.route('/')
def index():
    """Main page showing analysis results"""
    # Load existing results if any
    results = web_analyzer.load_results()

    # Check if there are videos to analyze
    video_files = glob.glob('input_videos/*.MOV') + glob.glob('input_videos/*.mov') + \
        glob.glob('input_videos/*.MP4') + glob.glob('input_videos/*.mp4') + \
        glob.glob('input_videos/*.AVI') + glob.glob('input_videos/*.avi')

    return render_template('index.html',
                           results=results,
                           video_files=[os.path.basename(
                               f) for f in video_files],
                           has_results=len(results) > 0)


@app.route('/analyze', methods=['POST'])
def run_analysis():
    """Run the cat behavior analysis"""
    try:
        results = web_analyzer.run_analysis()
        return jsonify({
            'success': True,
            'message': f'Analysis complete! Processed {len(results)} videos.',
            'results_count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Analysis failed: {str(e)}'
        })


@app.route('/results')
def show_results():
    """Show detailed results page"""
    results = web_analyzer.load_results()
    return render_template('results.html', results=results)


@app.route('/download')
def download_results():
    """Download all analysis results as ZIP"""
    try:
        zip_path = web_analyzer.create_download_package()
        return send_file(zip_path, as_attachment=True, download_name=os.path.basename(zip_path))
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


@app.route('/download/<path:filename>')
def download_file(filename):
    """Download individual files"""
    try:
        # Security check - only allow files from analysis folders
        allowed_folders = ['extracted_audio', 'audio_analysis_graphs',
                           'video_analysis_results', 'combined_analysis_results']

        folder = filename.split('/')[0] if '/' in filename else ''
        if folder not in allowed_folders:
            return jsonify({'error': 'Access denied'}), 403

        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


@app.route('/upload', methods=['POST'])
def upload_video():
    """Handle video file uploads"""
    try:
        if 'video_files' not in request.files:
            return jsonify({'success': False, 'message': 'No files selected'})

        files = request.files.getlist('video_files')
        uploaded_files = []

        # Create input_videos directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        for file in files:
            if file.filename == '':
                continue

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Check if file already exists
                if os.path.exists(file_path):
                    # Add timestamp to make filename unique
                    name, ext = os.path.splitext(filename)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{name}_{timestamp}{ext}"
                    file_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], filename)

                file.save(file_path)
                uploaded_files.append(filename)
            else:
                return jsonify({
                    'success': False,
                    'message': f'Invalid file type: {file.filename}. Allowed: MP4, AVI, MOV, MKV, WMV'
                })

        if uploaded_files:
            return jsonify({
                'success': True,
                'message': f'Successfully uploaded {len(uploaded_files)} video(s)',
                'files': uploaded_files
            })
        else:
            return jsonify({'success': False, 'message': 'No valid files uploaded'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Upload failed: {str(e)}'})


@app.route('/delete_video/<filename>', methods=['POST'])
def delete_video(filename):
    """Delete a video file"""
    try:
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'success': True, 'message': f'Deleted {filename}'})
        else:
            return jsonify({'success': False, 'message': 'File not found'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Delete failed: {str(e)}'})


@app.route('/toggle_ml', methods=['POST'])
def toggle_ml_analysis():
    """Toggle between traditional and ML analysis"""
    try:
        data = request.get_json()
        use_ml = data.get('use_ml', True)
        web_analyzer.use_ml = use_ml

        analysis_type = "Enhanced ML Analysis" if use_ml else "Traditional Analysis"
        return jsonify({
            'success': True,
            'message': f'Switched to {analysis_type}',
            'current_mode': analysis_type
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Toggle failed: {str(e)}'})


@app.route('/download_report')
def download_analysis_report():
    """Generate and download comprehensive analysis report"""
    try:
        results = web_analyzer.load_results()
        if not results:
            return jsonify({'error': 'No analysis results available'}), 404

        report_content = web_analyzer.generate_analysis_report(results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"cat_behavior_analysis_report_{timestamp}.txt"
        report_path = os.path.join('downloads', report_filename)

        # Create downloads directory
        os.makedirs('downloads', exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return send_file(report_path, as_attachment=True, download_name=report_filename)
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500


@app.route('/api/status')
def get_status():
    """Get current analysis status"""
    results = web_analyzer.load_results()
    video_files = glob.glob('input_videos/*.MOV') + glob.glob('input_videos/*.mov') + \
        glob.glob('input_videos/*.MP4') + glob.glob('input_videos/*.mp4') + \
        glob.glob('input_videos/*.AVI') + glob.glob('input_videos/*.avi') + \
        glob.glob('input_videos/*.MKV') + glob.glob('input_videos/*.mkv') + \
        glob.glob('input_videos/*.WMV') + glob.glob('input_videos/*.wmv')

    return jsonify({
        'videos_found': len(video_files),
        'results_available': len(results),
        'video_files': [os.path.basename(f) for f in video_files],
        'ml_available': ML_AVAILABLE,
        'current_mode': 'Enhanced ML' if web_analyzer.use_ml else 'Traditional'
    })


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('downloads', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    print("🌐 Starting Cat Behavior Analysis Web Interface...")
    print("📁 Access the interface at: http://localhost:5002")

    app.run(debug=False, host='0.0.0.0', port=5002)
