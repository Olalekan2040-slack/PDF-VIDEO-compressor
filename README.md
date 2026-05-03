# 🎬 Media Tool: PDF Compressor, Video Compressor & Auto Caption Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**A comprehensive Streamlit-based web application for media processing tasks including PDF compression, video compression, and automatic subtitle generation with burn-in capabilities. All processing is done locally on your machine for privacy and speed.**

[🚀 Quick Start](#-installation) • [📖 Features](#-features) • [🔧 Troubleshooting](#-troubleshooting) • [🤝 Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [🚀 Features](#-features)
- [🎨 Subtitle Features](#-subtitle-features)
- [🛠️ Requirements](#️-requirements)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [⚙️ Configuration](#️-configuration)
- [🔧 Troubleshooting](#-troubleshooting)
- [📁 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)
- [📞 Support](#-support)

---

## 🚀 Features

### 📄 PDF Compressor
- ✅ **Upload & Compress**: Support for PDF files with multiple compression levels
- 🎯 **Compression Levels**: Low (printer quality), Medium (ebook), High (screen)
- 🏠 **Local Processing**: Uses Ghostscript for efficient compression
- 📊 **Size Reduction Tracking**: Displays percentage of size reduction
- ⬇️ **Instant Download**: Compressed PDFs available for immediate download

### 🎬 Video Compressor
- 🎥 **Multi-Format Support**: MP4, MOV, AVI, MKV, WebM input formats
- 🔄 **Output Formats**: MP4 (H.264) and WebM (VP9) options
- ⚙️ **Quality Presets**: High Quality, Medium, Small Size with CRF settings
- ⚡ **Fast Processing**: Uses FFmpeg with optimized presets
- 📈 **Progress Feedback**: Real-time compression status

### 📝 Auto Caption Generator
- 🎙️ **Speech-to-Text**: Powered by Faster Whisper for accurate transcription
- 🧠 **Model Selection**: Choose from tiny, base, small, medium Whisper models
- 📝 **Sentence-Level Segmentation**: Natural sentence-based caption timing
- ✏️ **Interactive Editor**: Review and edit each caption sentence
- 📥 **SRT Export**: Download standard SRT subtitle files
- 🎬 **Video Burn-In**: Optional subtitle burning with animated slide-in effects
- 🎨 **Custom Styling**: Yellow text with black outline, Plus Jakarta Sans font

---

## 🎨 Subtitle Features

| Feature | Description |
|---------|-------------|
| 🎭 **Slide-In Animation** | Each subtitle slides in from the left edge of the screen |
| ⏰ **Precise Timing** | Captions appear exactly when speech begins |
| 📄 **ASS Format** | Advanced SubStation Alpha format for professional results |
| 📱 **Responsive Design** | Automatically adjusts to video resolution |
| 🔤 **Custom Font** | Plus Jakarta Sans, 32pt bold with yellow color scheme |

---

## 🛠️ Requirements

### System Dependencies

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Ghostscript** | PDF compression | Windows: `gswin64c.exe`<br>Linux/Mac: `apt install ghostscript` |
| **FFmpeg** | Video processing | Download from [ffmpeg.org](https://ffmpeg.org/download.html) |
| **Python 3.8+** | Application runtime | Download from [python.org](https://python.org) |

### Python Dependencies

```bash
streamlit>=1.28.0
faster-whisper>=0.10.0
```

---

## 📦 Installation

### Step 1: Clone or Download
```bash
git clone <repository-url>
cd pdf_compressor
```

### Step 2: Install Python Dependencies
```bash
pip install streamlit faster-whisper
```

### Step 3: Install System Tools

#### Ghostscript
- **Windows**: Usually comes with PDF viewers like Adobe Acrobat
- **Linux**: `sudo apt install ghostscript`
- **macOS**: `brew install ghostscript`

#### FFmpeg
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to system PATH

### Step 4: Verify Installation
```bash
# Test Ghostscript
gs --version

# Test FFmpeg
ffmpeg -version

# Test Python packages
python -c "import streamlit, faster_whisper; print('All good!')"
```

---

## 🚀 Usage

### Running the Application

1. Navigate to the project directory
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser to `http://localhost:8501`

### 📄 PDF Compression Workflow

<div align="center">

| Step | Action |
|------|--------|
| 1️⃣ | Select "📄 PDF Compressor" tab |
| 2️⃣ | Upload your PDF file |
| 3️⃣ | Choose compression level (Low/Medium/High) |
| 4️⃣ | Click "Compress PDF" |
| 5️⃣ | Download the compressed file |

</div>

### 🎬 Video Compression Workflow

<div align="center">

| Step | Action |
|------|--------|
| 1️⃣ | Select "🎬 Video Compressor" tab |
| 2️⃣ | Upload your video file |
| 3️⃣ | Select quality preset and output format |
| 4️⃣ | Click "Compress Video" |
| 5️⃣ | Download the compressed video |

</div>

### 📝 Auto Caption Generation Workflow

<div align="center">

| Step | Action |
|------|--------|
| 1️⃣ | Select "📝 Auto Captions" tab |
| 2️⃣ | Upload your video file |
| 3️⃣ | Choose Whisper model size |
| 4️⃣ | Check "Burn subtitles" if desired |
| 5️⃣ | Click "🎙️ Generate Captions" |
| 6️⃣ | Review and edit captions |
| 7️⃣ | Download SRT or captioned video |

</div>

---

## ⚙️ Configuration

### Whisper Models Comparison

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| **tiny** | ~39 MB | ⚡ Fastest | 📉 Lowest | Quick tests |
| **base** | ~74 MB | ⚡ Fast | 📊 Good | **Recommended** |
| **small** | ~244 MB | 🐌 Slow | 📈 Better | Quality priority |
| **medium** | ~769 MB | 🐌 Slowest | 📈 Best | Professional use |

### Video Burn-In Settings

```css
Font: Plus Jakarta Sans, 32pt, Bold
Color: Yellow (#F5C518) with black outline
Animation: Slide-in from left over 300ms
Position: Bottom center (88% down the frame)
```

---

## 🔧 Troubleshooting

### 🚨 Common Issues & Solutions

#### PDF Compression Issues
- **❌ Ghostscript not found**: Install Ghostscript and add to PATH
- **❌ Corrupted PDF**: Try with a different PDF file
- **❌ Compression fails**: Try different compression level

#### Video Processing Issues
- **❌ FFmpeg not found**: Install FFmpeg and add to PATH
- **❌ Unsupported format**: Check supported input formats
- **❌ No space**: Free up disk space for temporary files

#### Caption Generation Issues
- **❌ Import error**: `pip install faster-whisper`
- **❌ No audio track**: Ensure video has audio
- **❌ Memory error**: Use smaller Whisper model
- **💡 Tip**: Videos under 2 minutes process faster

#### Subtitle Burning Issues
- **❌ ASS filter missing**: Update FFmpeg to latest version
- **❌ Codec incompatibility**: Try different video codec
- **❌ Temp file error**: Check write permissions

### ⚡ Performance Optimization

- 🔸 Use smaller Whisper models for faster transcription
- 🔸 Process shorter videos (< 2 minutes) for quicker results
- 🔸 Close other applications to free up CPU/GPU resources
- 🔸 Use SSD storage for better performance
- 🔸 Lower video quality for faster compression

---

## 📁 Project Structure

```
pdf_compressor/
├── app.py                 # 🏠 Main Streamlit application
├── README.md             # 📖 This documentation
├── requirements.txt      # 📦 Python dependencies (optional)
└── .gitignore           # 🚫 Git ignore rules (optional)
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. 💻 **Make** your changes
4. 🧪 **Test** thoroughly
5. 📝 **Commit** your changes: `git commit -m 'Add amazing feature'`
6. 🚀 **Push** to the branch: `git push origin feature/amazing-feature`
7. 🔄 **Open** a Pull Request

### Development Setup
```bash
# Clone the repo
git clone <repository-url>
cd pdf_compressor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app.py --server.headless true
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```text
MIT License - Free to use, modify, and distribute.
```

---

## 🙏 Acknowledgments

<div align="center">

**Special thanks to the amazing open-source projects that make this possible:**

| Project | Purpose | Link |
|---------|---------|------|
| **Streamlit** | Web app framework | [streamlit.io](https://streamlit.io) |
| **Faster Whisper** | Speech recognition | [github.com/SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) |
| **FFmpeg** | Video processing | [ffmpeg.org](https://ffmpeg.org) |
| **Ghostscript** | PDF compression | [ghostscript.com](https://ghostscript.com) |
| **Plus Jakarta Sans** | Typography | [fonts.google.com](https://fonts.google.com/specimen/Plus+Jakarta+Sans) |

</div>

---

## 📞 Support

### Getting Help

If you encounter issues or have questions:

1. 📖 **Check** the [Troubleshooting](#-troubleshooting) section above
2. 🔍 **Verify** all dependencies are properly installed
3. 🧪 **Test** with smaller files first
4. 🐛 **Report** issues with detailed error messages and system info

### Feature Requests

Have an idea for a new feature? We'd love to hear it!

- 🐛 **Bug Reports**: [Open an Issue](https://github.com/your-repo/issues)
- 💡 **Feature Requests**: [Open an Issue](https://github.com/your-repo/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

<div align="center">

### 🎯 Quick Tips

- **For PDFs**: Use "Medium" compression for best balance
- **For Videos**: Try "High Quality" first, then adjust
- **For Captions**: Use "base" model for speed/accuracy balance
- **Best Results**: Videos under 2 minutes process fastest

---

**Made with ❤️ for media creators and content producers**

[⬆️ Back to Top](#-media-tool-pdf-compressor-video-compressor--auto-caption-generator)

</div>