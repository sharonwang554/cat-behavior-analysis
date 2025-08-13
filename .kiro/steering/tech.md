# Technology Stack & Build System

## Core Technologies

### Backend

- **Python 3.7+** - Core analysis engine
- **Flask** - Web framework for user interface
- **librosa** - Audio processing and feature extraction
- **OpenCV (cv2)** - Video processing and computer vision
- **NumPy/SciPy** - Numerical computing and signal processing
- **matplotlib** - Data visualization and plotting
- **scikit-learn** - Machine learning features and ensemble methods
- **moviepy** - Video/audio manipulation (full version)
- **TensorFlow** - Deep learning and neural networks for advanced ML analysis
- **joblib** - Model persistence and parallel processing

### Frontend

- **HTML5/CSS3** - Web interface templates
- **Vanilla JavaScript** - Client-side interactions
- **Jinja2** - Template engine (Flask default)

### System Dependencies

- **FFmpeg** - Audio extraction from video files
- **soundfile** - Audio file I/O operations

## Project Structure

### Analysis Modules

- `analysis.py` - Original audio-only meow analysis
- `video_analysis.py` - Complete video + audio analysis (uses moviepy)
- `simple_video_analysis.py` - Streamlined analysis (uses ffmpeg directly)
- `enhanced_video_analysis.py` - Advanced ML-enhanced analysis combining traditional and neural network methods
- `ml_analysis.py` - Pure machine learning analysis with neural networks and ensemble methods
- `web_app.py` - Flask web application with ML integration

### Setup & Utilities

- `setup_video_analysis.py` - Dependency installer and folder structure creator
- `start_web_interface.py` - Web interface startup script

## Common Commands

### Initial Setup

```bash
# Automatic setup with virtual environment (recommended)
./run_web_interface.sh

# Manual setup
python3.11 -m venv cat_analysis_env
source cat_analysis_env/bin/activate
pip install -r requirements.txt
```

### Running the Application

```bash
# Web interface (recommended)
./run_web_interface.sh
# Access at http://localhost:5002

# Command line analysis options
python3 video_analysis.py              # Traditional analysis
python3 enhanced_video_analysis.py     # ML-enhanced analysis
python3 simple_video_analysis.py       # Lightweight analysis

# Simplified analysis (fewer dependencies)
python3 simple_video_analysis.py
```

### Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run web app directly
python3 web_app.py

# Test audio analysis only
python3 analysis.py
```

## Architecture Patterns

### Modular Design

- Separate modules for audio analysis, video analysis, and web interface
- Reusable analysis functions imported across modules
- Clear separation between analysis engine and presentation layer

### File Organization

- Input files in `input_videos/`
- Processed outputs organized by type in dedicated folders
- Web interface serves files securely from analysis output folders only

### Error Handling

- Graceful degradation (video-only analysis if audio extraction fails)
- Comprehensive try-catch blocks with user-friendly error messages
- Fallback to simpler methods when advanced processing fails
