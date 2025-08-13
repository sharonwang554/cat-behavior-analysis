#!/usr/bin/env python3
"""
Cat Behavior Analysis Web Interface
Displays analysis results on a webpage with download options
"""

from flask import Flask, render_template, send_file, request, jsonify, redirect, url_for, flash
import os
import json
import shutil
import zipfile
from datetime import datetime
import glob
from werkzeug.utils import secure_filename
from simple_video_analysis import SimpleCatVideoAnalyzer

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
        self.results_cache = {}

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

        # Run the analysis
        self.analyzer.analyze_all_videos()

        # Cache the results
        self.load_results()

        return self.results_cache

    def load_results(self):
        """Load analysis results from JSON files"""
        self.results_cache = {}

        json_files = glob.glob('combined_analysis_results/*.json')
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    video_name = data.get('video_name', os.path.splitext(
                        os.path.basename(json_file))[0])
                    self.results_cache[video_name] = data
            except Exception as e:
                print(f"Error loading {json_file}: {e}")

        return self.results_cache

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
        'video_files': [os.path.basename(f) for f in video_files]
    })


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('downloads', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    print("🌐 Starting Cat Behavior Analysis Web Interface...")
    print("📁 Access the interface at: http://localhost:5001")

    app.run(debug=False, host='0.0.0.0', port=5001)
