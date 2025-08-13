# 🐱 Cat Behavior Analysis System

A comprehensive AI-powered system for analyzing cat behavior through both audio (meow analysis) and video (movement/activity analysis) with an easy-to-use web interface.

## ✨ Features

### 🌐 Web Interface

- **User-friendly dashboard** at `http://localhost:5001`
- **Drag & drop video upload** directly in the browser
- **Real-time analysis progress** with visual feedback
- **Interactive results display** with color-coded confidence levels
- **One-click downloads** for complete analysis packages or individual files
- **Automatic cleanup** of previous results when re-running analysis

### 🎵 Advanced Audio Analysis

- **Cat-specific filtering** isolates vocalizations from background noise
- **Pitch pattern analysis** identifies emotional states
- **Duration analysis** distinguishes short greetings from long complaints
- **Loudness analysis** detects gentle requests vs demanding calls
- **Spectral analysis** provides voice quality and emotional indicators
- **Behavioral interpretation** categorizes attention-seeking, distress, and general communication

### 🎥 Comprehensive Video Analysis

- **Movement tracking** monitors activity levels over time
- **Scene analysis** considers environmental context and lighting
- **Activity classification** categorizes high/medium/low activity periods
- **Temporal patterns** shows how behavior changes throughout videos

### 🧠 Combined Intelligence

- **Audio-visual correlation** links vocalizations with visual behavior
- **Behavioral recommendations** provides actionable insights for cat care
- **Confidence scoring** indicates reliability of analysis results

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

1. **Setup the environment:**

   ```bash
   python3 setup_video_analysis.py
   ```

2. **Start the web interface:**

   ```bash
   python3 start_web_interface.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5001`

4. **Upload and analyze:**
   - Drag & drop your cat videos or click to select files
   - Click "Start Analysis"
   - View results and download analysis packages

### Option 2: Command Line

1. **Setup:**

   ```bash
   python3 setup_video_analysis.py
   ```

2. **Add videos to input_videos/ folder**

3. **Run analysis:**
   ```bash
   python3 video_analysis.py
   ```

## 📁 Project Structure

```
├── 🌐 Web Interface
│   ├── web_app.py                     # Flask web application
│   ├── start_web_interface.py         # Web interface startup script
│   └── templates/                     # HTML templates
│       ├── base.html                  # Main template with upload functionality
│       ├── index.html                 # Dashboard page
│       └── results.html               # Detailed results page
│
├── 🧠 Analysis Engine
│   ├── analysis.py                    # Original audio-only meow analysis
│   ├── simple_video_analysis.py       # Streamlined video + audio analysis
│   ├── video_analysis.py             # Complete video + audio analysis
│   └── setup_video_analysis.py       # Setup script and dependency installer
│
├── 📁 Data Folders
│   ├── input_videos/                  # Upload your cat videos here
│   ├── extracted_audio/               # Audio files extracted from videos
│   ├── audio_analysis_graphs/         # Audio analysis visualizations
│   ├── video_analysis_results/        # Video movement analysis plots
│   ├── combined_analysis_results/     # Complete behavioral analysis (JSON)
│   └── downloads/                     # Generated ZIP packages
│
└── 📚 Documentation
    ├── README.md                      # This file
    ├── VIDEO_ANALYSIS_GUIDE.md        # Detailed analysis guide
    ├── WEB_INTERFACE_README.md        # Web interface documentation
    └── requirements.txt               # Python dependencies
```

## 🎯 Supported Video Formats

- **MP4** - Most common, best compatibility
- **MOV** - Apple/iPhone videos
- **AVI** - Windows standard
- **MKV** - High quality container
- **WMV** - Windows Media Video

**File size limit:** 500MB per video

## 📊 What Gets Analyzed

### 🎵 Audio Features

- **Frequency Analysis**: Pitch patterns and tonal qualities
- **Temporal Analysis**: Duration and timing of vocalizations
- **Amplitude Analysis**: Volume levels and intensity variations
- **Spectral Analysis**: Voice quality and harmonic content
- **Emotional Classification**: Happy, distressed, attention-seeking, etc.

### 🎥 Visual Features

- **Movement Detection**: Activity levels and motion patterns
- **Brightness Analysis**: Environmental lighting conditions
- **Activity Classification**: High/medium/low energy periods
- **Temporal Correlation**: How visual activity relates to vocalizations

### 🧠 Combined Insights

- **Behavioral Correlation**: Links audio and visual cues
- **Mood Assessment**: Overall emotional state interpretation
- **Care Recommendations**: Actionable insights for pet owners
- **Confidence Scoring**: Reliability indicators for all analyses

## 🛠 Installation & Dependencies

### Automatic Setup (Recommended)

```bash
python3 setup_video_analysis.py
```

### Manual Installation

```bash
pip install -r requirements.txt
```

### System Requirements

- **Python 3.7+**
- **FFmpeg** (for audio extraction)
- **Modern web browser** (for web interface)
- **2GB+ RAM** (for video processing)
- **Sufficient disk space** for temporary files

## 💡 Usage Tips

1. **Video Quality**: Clear audio and good lighting improve analysis accuracy
2. **File Organization**: The system automatically organizes all output files
3. **Batch Processing**: Upload multiple videos for comprehensive analysis
4. **Results Interpretation**: Higher confidence scores indicate more reliable results
5. **Cleanup**: Previous results are automatically cleared when re-running analysis

## 🔧 Troubleshooting

### Common Issues

- **No audio extracted**: Ensure FFmpeg is installed and videos contain audio tracks
- **Analysis fails**: Check video file integrity and supported formats
- **Web interface not loading**: Verify port 5001 is available
- **Upload fails**: Check file size limits (500MB max) and format support

### Getting Help

- Check the detailed guides in `VIDEO_ANALYSIS_GUIDE.md` and `WEB_INTERFACE_README.md`
- Ensure all dependencies are installed via `setup_video_analysis.py`
- Verify video files are in supported formats and contain audio

## 🎯 Perfect For

- **Pet Owners**: Understanding your cat's communication and behavior
- **Veterinarians**: Professional behavioral assessment tools
- **Researchers**: Batch processing with downloadable scientific data
- **Cat Behaviorists**: Detailed acoustic and visual analysis tools

## 🔒 Privacy & Security

- **Local Processing**: All analysis happens on your machine
- **No Data Upload**: Videos and results never leave your computer
- **Secure Downloads**: File access restricted to analysis output folders
- **No External Dependencies**: Works completely offline after setup

## 📈 Technical Details

Built with:

- **Python 3.7+** for core analysis
- **Flask** for web interface
- **librosa** for audio processing
- **OpenCV** for video analysis
- **matplotlib** for visualizations
- **scikit-learn** for machine learning features

## 🤝 Contributing

This is an open-source project. Feel free to:

- Report bugs and issues
- Suggest new features
- Submit pull requests
- Share your analysis results

## 📄 License

Open source - feel free to use, modify, and distribute.

---

**Made with ❤️ for cat lovers and their feline friends** 🐱

### Combined Analysis

- **Behavior correlation**: Links vocalizations with visual activity
- **Mood interpretation**: Overall emotional state assessment
- **Recommendations**: Actionable insights for cat care

## 📈 Output Files

### Audio Analysis

- `extracted_audio/`: WAV files extracted from videos
- `audio_analysis_graphs/`: Spectrograms, pitch contours, MFCC analysis

### Video Analysis

- `video_analysis_results/`: Movement plots, activity distributions

### Combined Results

- `combined_analysis_results/`: JSON files with complete behavioral analysis

## 🔧 Technical Details

### Dependencies

- **librosa**: Audio analysis and feature extraction
- **opencv-python**: Video processing and computer vision
- **moviepy**: Video/audio manipulation
- **matplotlib**: Visualization and plotting
- **numpy/scipy**: Numerical computing

### Analysis Pipeline

1. **Video Input**: Load cat video file
2. **Audio Extraction**: Extract audio track to WAV format
3. **Audio Analysis**: Apply existing meow analysis algorithms
4. **Frame Analysis**: Process video frames for movement detection
5. **Correlation**: Combine audio and visual insights
6. **Interpretation**: Generate behavioral recommendations
7. **Output**: Save graphs, data, and interpretations

## 🎯 Use Cases

- **Pet Behavior Monitoring**: Understand your cat's communication patterns
- **Veterinary Assessment**: Detect potential distress or health issues
- **Research Applications**: Study feline behavior and communication
- **Pet Care Optimization**: Get actionable recommendations for cat care

## ⚠️ Limitations

- Analysis is based on general cat behavior patterns
- Individual cats may have unique characteristics
- Video quality affects analysis accuracy
- Not a substitute for professional veterinary advice

## 🔄 Extending the System

The modular design allows for easy extensions:

- Add new audio features to `analysis.py`
- Enhance video analysis in `video_analysis.py`
- Implement machine learning models for better accuracy
- Add support for multiple cats in one video
