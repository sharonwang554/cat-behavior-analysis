# 🎬 Cat Video Analysis Guide

## Quick Start

### 1. Setup (Already Done!)

The system is ready to use with these folders created:

- `input_videos/` - Place your cat videos here
- `extracted_audio/` - Audio files extracted from videos
- `audio_analysis_graphs/` - Audio analysis visualizations
- `video_analysis_results/` - Video movement analysis plots
- `combined_analysis_results/` - Complete behavioral analysis (JSON)

### 2. Add Your Videos

Place cat videos in the `input_videos/` folder. Supported formats:

- MP4, AVI, MOV, MKV, WMV

### 3. Run Analysis

```bash
# For full video + audio analysis (requires ffmpeg)
python3 simple_video_analysis.py

# For audio-only analysis of existing audio files
python3 analysis.py
```

## What Gets Analyzed

### 🎵 Audio Analysis

- **Pitch patterns**: Frequency analysis of meows
- **Duration**: Short vs long vocalizations
- **Loudness**: Volume and intensity patterns
- **Spectral features**: Voice quality indicators
- **Emotional interpretation**: Attention-seeking, distress, etc.

### 🎥 Video Analysis

- **Movement tracking**: Activity levels over time
- **Scene analysis**: Brightness and environmental context
- **Activity classification**: High/Medium/Low activity periods
- **Temporal patterns**: How behavior changes throughout video

### 🧠 Combined Analysis

- **Behavioral correlation**: Links vocalizations with visual activity
- **Mood assessment**: Overall emotional state interpretation
- **Recommendations**: Actionable insights for cat care

## Output Files

### Generated Graphs

- `audio_analysis_graphs/`: Spectrograms, pitch analysis, MFCC features
- `video_analysis_results/`: Movement plots, activity distributions

### Data Files

- `extracted_audio/`: WAV files from video audio tracks
- `combined_analysis_results/`: JSON files with complete analysis

## Example Analysis Results

```
🐱 COMPREHENSIVE CAT BEHAVIOR ANALYSIS 🐱

📹 Video: my_cat_video
⏱️  Duration: 15.3 seconds
🎵 Audio Emotion: Seeking attention/affection
📊 Visual Activity: High

🧠 COMBINED INTERPRETATION:
Overall Mood: Playful and attention-seeking
Behavior Pattern: Active communication
Analysis Confidence: High

💡 RECOMMENDATIONS:
• Engage in interactive play
```

## Troubleshooting

### No Audio Analysis

If audio extraction fails:

- Install ffmpeg: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)
- Check video has audio track
- Video analysis will continue without audio

### Video Analysis Issues

- Ensure video file is not corrupted
- Check supported formats (MP4 recommended)
- Large videos may take longer to process

### Dependencies

If you get import errors:

```bash
pip3 install opencv-python-headless matplotlib numpy
```

## Understanding the Analysis

### Audio Interpretation

- **High pitch + Long duration** = Demanding attention/food
- **Low pitch + Stable** = Calm communication
- **Rough/raspy** = Possible distress
- **Short bursts** = Greetings or acknowledgments

### Visual Interpretation

- **High movement + Vocalizations** = Active play/attention seeking
- **Low movement + Vocalizations** = Gentle requests
- **High movement + No audio** = Independent play
- **Low movement + Distressed audio** = Possible health concern

### Combined Insights

The system correlates timing of vocalizations with movement patterns to provide more accurate behavioral assessment than either analysis alone.

## Advanced Usage

### Batch Processing

The system automatically processes all videos in `input_videos/` folder.

### Custom Analysis

Modify thresholds in `simple_video_analysis.py`:

- Movement sensitivity (line ~95)
- Activity level boundaries (lines ~100-106)
- Audio interpretation rules (in `analysis.py`)

### Integration

JSON output files can be used with other tools for:

- Behavioral trend analysis
- Health monitoring dashboards
- Research data collection
