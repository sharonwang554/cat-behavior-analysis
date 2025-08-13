# 🌐 Cat Behavior Analysis Web Interface

A user-friendly web interface for the Cat Behavior Analysis System that displays results on a webpage with download options.

## 🚀 Quick Start

### 1. Start the Web Interface

```bash
python3 start_web_interface.py
```

### 2. Access the Interface

Open your web browser and go to: **http://localhost:5000**

### 3. Add Videos

Place your cat videos (.MOV, .MP4, .AVI, etc.) in the `input_videos/` folder

### 4. Run Analysis

Click the "Start Analysis" button on the web interface

## ✨ Features

### 📊 **Interactive Dashboard**

- Real-time analysis status
- Visual results display with color-coded confidence levels
- Responsive design that works on desktop and mobile

### 📥 **Download Options**

- **Complete Package**: Download all results as a ZIP file
- **Individual Files**: Download specific analysis graphs and data
- **Automatic Cleanup**: Previous results are cleared when re-running analysis

### 🎯 **Analysis Results Display**

- **Audio Analysis**: Emotional state, urgency level, primary meaning
- **Video Analysis**: Activity levels, movement patterns, duration
- **Combined Insights**: Behavioral interpretation and recommendations
- **Confidence Indicators**: Color-coded badges showing analysis reliability

### 🔄 **Automatic Cleanup**

- Previous analysis results are automatically removed when starting a new analysis
- Keeps the system clean and prevents confusion between different runs
- Extracted audio files, graphs, and data are all cleared

## 📁 **File Organization**

The web interface automatically organizes files into:

```
├── input_videos/              # Place your cat videos here
├── extracted_audio/           # Audio segments (auto-cleaned)
├── audio_analysis_graphs/     # Audio analysis plots (auto-cleaned)
├── video_analysis_results/    # Video analysis plots (auto-cleaned)
├── combined_analysis_results/ # JSON data files (auto-cleaned)
├── downloads/                 # Generated ZIP packages
└── templates/                 # Web interface templates
```

## 🎨 **Web Interface Pages**

### **Main Dashboard** (`/`)

- Shows videos found in input_videos/ folder
- Analysis status and controls
- Quick results overview
- Download options

### **Detailed Results** (`/results`)

- Complete analysis breakdown for each video
- Individual file download options
- Behavioral recommendations
- Analysis timestamps

## 🔧 **API Endpoints**

- `GET /` - Main dashboard
- `POST /analyze` - Start analysis (AJAX)
- `GET /results` - Detailed results page
- `GET /download` - Download complete ZIP package
- `GET /download/<filename>` - Download individual files
- `GET /api/status` - Get current status (JSON)

## 💡 **Usage Tips**

1. **Video Formats**: Supports MP4, MOV, AVI, MKV, WMV
2. **File Size**: Maximum 500MB per video file
3. **Analysis Time**: Depends on video length and number of files
4. **Browser Compatibility**: Works with modern browsers (Chrome, Firefox, Safari, Edge)
5. **Mobile Friendly**: Responsive design works on phones and tablets

## 🛠 **Troubleshooting**

### **No Videos Found**

- Check that videos are in the `input_videos/` folder
- Ensure files have supported extensions (.MOV, .MP4, etc.)
- Refresh the page after adding videos

### **Analysis Fails**

- Check that ffmpeg is installed for audio extraction
- Ensure sufficient disk space for temporary files
- Check browser console for error messages

### **Download Issues**

- Large ZIP files may take time to generate
- Check that analysis completed successfully
- Try downloading individual files if ZIP fails

## 🔒 **Security Notes**

- The web interface only allows access to analysis result files
- File downloads are restricted to the analysis output folders
- No file upload functionality (videos must be placed manually in input_videos/)

## 🎯 **Perfect For**

- **Pet Owners**: Easy-to-understand analysis of your cat's behavior
- **Veterinarians**: Professional behavioral assessment tools
- **Researchers**: Batch processing with downloadable data
- **Cat Behaviorists**: Detailed acoustic and visual analysis

The web interface makes the powerful cat behavior analysis system accessible to everyone, with no command-line knowledge required!
