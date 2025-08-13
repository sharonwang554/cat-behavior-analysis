# Project Structure & Organization

## Directory Layout

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
├── 📁 Data Folders (Auto-created)
│   ├── input_videos/                  # Upload your cat videos here
│   ├── extracted_audio/               # Audio files extracted from videos
│   ├── audio_analysis_graphs/         # Audio analysis visualizations
│   ├── video_analysis_results/        # Video movement analysis plots
│   ├── combined_analysis_results/     # Complete behavioral analysis (JSON)
│   └── downloads/                     # Generated ZIP packages
│
├── 📚 Configuration & Dependencies
│   ├── requirements.txt               # Python dependencies
│   └── .gitignore                     # Git ignore patterns
│
└── 📖 Documentation
    ├── README.md                      # Main project documentation
    ├── VIDEO_ANALYSIS_GUIDE.md        # Detailed analysis guide
    └── WEB_INTERFACE_README.md        # Web interface documentation
```

## File Naming Conventions

### Analysis Files

- `analysis.py` - Core audio analysis functions
- `*_analysis.py` - Analysis modules (video_analysis, simple_video_analysis)
- `*_analysis_*.png` - Generated analysis graphs
- `*_combined_analysis.json` - Complete analysis results

### Video Files

- Input videos: Any supported format (MP4, MOV, AVI, MKV, WMV)
- Extracted audio: `{video_name}_audio.wav`
- Audio segments: `{video_name}_meow_segment_{n}.wav`

### Web Interface

- `web_app.py` - Main Flask application
- `start_*.py` - Startup scripts
- Templates follow Flask conventions in `templates/` folder

## Data Flow

### Input Processing

1. Videos placed in `input_videos/` (manually or via web upload)
2. Audio extracted to `extracted_audio/`
3. Audio segments isolated and saved with sequential naming

### Analysis Pipeline

1. Audio analysis generates graphs in `audio_analysis_graphs/`
2. Video analysis generates plots in `video_analysis_results/`
3. Combined results saved as JSON in `combined_analysis_results/`

### Output Organization

- All analysis outputs organized by type in dedicated folders
- Web interface creates downloadable ZIP packages in `downloads/`
- Automatic cleanup of previous results when re-running analysis

## Code Organization Patterns

### Class Structure

- `CatVideoAnalyzer` - Full-featured analysis with moviepy
- `SimpleCatVideoAnalyzer` - Streamlined analysis with ffmpeg
- `WebCatAnalyzer` - Web interface wrapper class

### Function Naming

- `analyze_*` - Core analysis functions
- `extract_*` - Data extraction functions
- `create_*` - File/visualization creation functions
- `setup_*` - Initialization and setup functions

### Import Patterns

- Analysis functions imported from `analysis.py` into video analysis modules
- Web app imports analysis classes for processing
- Shared utilities and constants defined in main modules

## Security Considerations

### File Access

- Web interface only serves files from designated analysis output folders
- Secure filename handling with `secure_filename()`
- File type validation for uploads

### Data Privacy

- All processing happens locally
- No external API calls or data transmission
- Automatic cleanup options available
