# Technology Stack & Build System

## Core Technologies

### Backend

- **Python 3.7+** - Core analysis engine
- **Flask** - Web framework for user interface
- **librosa** - Audio processing and feature extraction
- **OpenCV (cv2)** - Video processing and computer vision
- **NumPy/SciPy** - Numerical computing and signal processing
- **matplotlib** - Data visualization and plotting
- **scikit-learn** - Machine learning features
- **moviepy** - Video/audio manipulation (full version)

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
- `web_app.py` - Flask web application

### Setup & Utilities

- `setup_video_analysis.py` - Dependency installer and folder structure creator
- `start_web_interface.py` - Web interface startup script

## Common Commands

### Initial Setup

```bash
# Automatic setup (recommended)
python3 setup_video_analysis.py

# Manual dependency installation
pip install -r requirements.txt
```

### Running the Application

```bash
# Web interface (recommended)
python3 start_web_interface.py
# Access at http://localhost:5001

# Command line analysis
python3 video_analysis.py

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
