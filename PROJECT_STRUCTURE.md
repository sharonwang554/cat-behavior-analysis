# 🐱 Cat Behavior Analysis System - Project Structure

## 📁 Main Project Files

### Core Analysis Files

- `analysis.py` - Core audio analysis functions and meow interpretation
- `video_analysis.py` - Complete video + audio analysis with moviepy
- `simple_video_analysis.py` - Streamlined analysis with ffmpeg
- `enhanced_video_analysis.py` - ML-enhanced analysis combining traditional and neural networks
- `ml_analysis.py` - Pure machine learning analysis with neural networks

### Web Interface

- `web_app.py` - Flask web application with ML integration
- `start_web_interface.py` - Web interface startup script
- `run_web_interface.sh` - Shell script to start web interface
- `templates/` - HTML templates for web interface
- `static/` - CSS, JavaScript, and other static assets

### Setup and Configuration

- `setup_video_analysis.py` - Dependency installer and folder structure creator
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore patterns

### Documentation

- `README.md` - Main project documentation
- `docs/` - Additional documentation files
  - `VIDEO_ANALYSIS_GUIDE.md` - Detailed analysis guide
  - `WEB_INTERFACE_README.md` - Web interface documentation
  - `ML_ANALYSIS_README.md` - Machine learning analysis documentation
  - `ADVANCED_FEATURES_IMPLEMENTED.md` - Advanced features documentation
  - `ENHANCED_ANALYSIS_SUMMARY.md` - Enhanced analysis summary
  - `SYSTEM_STATUS_REPORT.md` - System status and capabilities
  - `FINAL_BUG_FIXES_REPORT.md` - Bug fixes and resolutions
  - `CODEBASE_FIXES_SUMMARY.md` - Summary of codebase improvements
  - `BACKGROUND_FIX_SUMMARY.md` - Background color fix documentation
  - `PURPLE_COLOR_FIX_SUMMARY.md` - Purple color fix documentation
  - `PURPLE_BACKGROUND_VISIBILITY_FIX.md` - Background visibility improvements
  - `WEB_INTERFACE_FIXES.md` - Web interface bug fixes
  - `WEB_INTERFACE_IMPROVEMENTS.md` - Web interface improvements

### Test Files

- `tests/` - Test scripts and utilities
  - `test_advanced_features.py` - Advanced vocal patterns testing
  - `test_enhanced_analysis.py` - Enhanced analysis testing
  - `test_web_fixes.py` - Web interface fixes testing
  - `test_color_assignment.py` - Color assignment testing
  - `test_template_fix.py` - Template fix testing
  - `test_background_fix.py` - Background fix testing
  - `test_purple_background_fix.py` - Purple background testing
  - `create_test_result.py` - Test data creation utility

## 📁 Data Folders (Auto-created)

### Input and Processing

- `input_videos/` - Upload your cat videos here
- `extracted_audio/` - Audio files extracted from videos
- `extracted_features/` - ML feature extraction results

### Analysis Results

- `audio_analysis_graphs/` - Audio analysis visualizations
- `video_analysis_results/` - Video movement analysis plots
- `combined_analysis_results/` - Complete behavioral analysis (JSON)
- `ml_analysis_results/` - Machine learning analysis results
- `ml_models/` - Trained ML models
- `training_data/` - Training data for ML models

### Output and Downloads

- `downloads/` - Generated ZIP packages for download
- `audio_samples/` - Audio sample files

## 🚀 Quick Start

### 1. Setup

```bash
python3 setup_video_analysis.py
```

### 2. Web Interface (Recommended)

```bash
./run_web_interface.sh
# or
python3 start_web_interface.py
```

Access at: http://localhost:5002

### 3. Command Line Analysis

```bash
# Complete analysis
python3 video_analysis.py

# Enhanced ML analysis
python3 enhanced_video_analysis.py

# Simple analysis
python3 simple_video_analysis.py

# Audio only
python3 analysis.py
```

## 🎯 Supported Video Formats

- MP4, MOV, AVI, MKV, WMV
- Max file size: 500MB per video

## 📊 Analysis Features

- **Audio Analysis**: Meow detection, pitch analysis, emotional state classification
- **Video Analysis**: Movement tracking, activity level detection
- **ML Analysis**: Neural network behavioral classification
- **Combined Analysis**: Audio-visual correlation and behavioral insights
- **Web Interface**: User-friendly dashboard with real-time analysis

## 🔧 Development

- **Tests**: Run tests from `tests/` folder
- **Documentation**: Additional docs in `docs/` folder
- **Configuration**: Modify `config.py` for settings
- **Styling**: Update `static/css/main.scss` and compile to CSS

## 📝 Notes

- All analysis results are stored locally (no external data transmission)
- The system automatically creates necessary folders on first run
- Web interface provides the most user-friendly experience
- Command line tools are available for batch processing and automation
