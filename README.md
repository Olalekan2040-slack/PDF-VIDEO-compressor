# Media Tool: PDF Compressor, Video Compressor & Auto Caption Generator

A comprehensive Streamlit-based web application for media processing tasks including PDF compression, video compression, and automatic subtitle generation with burn-in capabilities. All processing is done locally on your machine for privacy and speed.

## 🚀 Features

### 📄 PDF Compressor
- **Upload & Compress**: Support for PDF files with multiple compression levels
- **Compression Levels**: Low (printer quality), Medium (ebook), High (screen)
- **Local Processing**: Uses Ghostscript for efficient compression
- **Size Reduction Tracking**: Displays percentage of size reduction
- **Instant Download**: Compressed PDFs available for immediate download

### 🎬 Video Compressor
- **Multi-Format Support**: MP4, MOV, AVI, MKV, WebM input formats
- **Output Formats**: MP4 (H.264) and WebM (VP9) options
- **Quality Presets**: High Quality, Medium, Small Size with CRF settings
- **Fast Processing**: Uses FFmpeg with optimized presets
- **Progress Feedback**: Real-time compression status

### 📝 Auto Caption Generator
- **Speech-to-Text**: Powered by Faster Whisper for accurate transcription
- **Model Selection**: Choose from tiny, base, small, medium Whisper models
- **Sentence-Level Segmentation**: Natural sentence-based caption timing
- **Interactive Editor**: Review and edit each caption sentence
- **SRT Export**: Download standard SRT subtitle files
- **Video Burn-In**: Optional subtitle burning with animated slide-in effects
- **Custom Styling**: Yellow text with black outline, Plus Jakarta Sans font

## 🎨 Subtitle Features

- **Slide-In Animation**: Each subtitle slides in from the left edge of the screen
- **Precise Timing**: Captions appear exactly when speech begins
- **ASS Format**: Advanced SubStation Alpha format for professional results
- **Responsive Design**: Automatically adjusts to video resolution
- **Custom Font**: Plus Jakarta Sans, 32pt bold with yellow color scheme

## 🛠️ Requirements

### System Dependencies
- **Ghostscript**: For PDF compression
  - Windows: `gswin64c.exe` (comes with many PDF viewers)
  - Linux/Mac: Install via package manager (`apt install ghostscript`, `brew install ghostscript`)
- **FFmpeg**: For video processing
  - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
  - Add to system PATH
- **Python 3.8+**: Required for running the application

### Python Dependencies
```
streamlit>=1.28.0
faster-whisper>=0.10.0
```

## 📦 Installation

1. **Clone or Download** the project files to your local machine

2. **Install Python Dependencies**:
   ```bash
   pip install streamlit faster-whisper
   ```

3. **Install System Tools**:
   - **Ghostscript**: Ensure `gs` (Linux/Mac) or `gswin64c.exe` (Windows) is in your PATH
   - **FFmpeg**: Ensure `ffmpeg` and `ffprobe` are in your PATH

4. **Verify Installation**:
   ```bash
   # Test Ghostscript
   gs --version
   
   # Test FFmpeg
   ffmpeg -version
   ```

## 🚀 Usage

### Running the Application

1. Navigate to the project directory
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser to the displayed URL (typically `http://localhost:8501`)

### PDF Compression
1. Select the "📄 PDF Compressor" tab
2. Upload your PDF file
3. Choose compression level (Low/Medium/High)
4. Click "Compress PDF"
5. Download the compressed file

### Video Compression
1. Select the "🎬 Video Compressor" tab
2. Upload your video file
3. Select quality preset and output format
4. Click "Compress Video"
5. Download the compressed video

### Auto Caption Generation
1. Select the "📝 Auto Captions" tab
2. Upload your video file
3. Choose Whisper model size (base recommended for balance)
4. Optionally check "Burn subtitles into video"
5. Click "🎙️ Generate Captions"
6. Review and edit captions in the interactive editor
7. Download SRT file or burn subtitles into video

## ⚙️ Configuration

### Whisper Models
- **tiny**: Fastest, least accurate (~39 MB)
- **base**: Good balance, recommended (~74 MB)
- **small**: Better accuracy (~244 MB)
- **medium**: High accuracy (~769 MB)

### Video Burn-In Settings
- Font: Plus Jakarta Sans, 32pt, Bold
- Color: Yellow (#F5C518) with black outline
- Animation: Slide-in from left over 300ms
- Position: Bottom center (88% down the frame)

## 🔧 Troubleshooting

### Common Issues

**PDF Compression Fails**
- Ensure Ghostscript is installed and in PATH
- Check that the PDF file is not corrupted
- Try a different compression level

**Video Compression Fails**
- Verify FFmpeg installation
- Ensure input video format is supported
- Check available disk space

**Caption Generation Fails**
- Install faster-whisper: `pip install faster-whisper`
- Ensure video has audio track
- Try a smaller Whisper model if memory issues occur
- Videos under 2 minutes process faster

**Burning Subtitles Fails**
- Ensure FFmpeg supports ASS filter
- Check video codec compatibility
- Verify sufficient disk space for temporary files

### Performance Tips
- Use smaller Whisper models for faster transcription
- Process shorter videos for quicker results
- Close other applications to free up CPU/GPU resources
- Use SSD storage for better performance

## 📁 Project Structure

```
pdf_compressor/
├── app.py              # Main Streamlit application
├── README.md           # This file
└── requirements.txt    # Python dependencies (optional)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web app framework
- **Faster Whisper**: For fast and accurate speech recognition
- **FFmpeg**: For powerful video processing capabilities
- **Ghostscript**: For reliable PDF compression
- **Plus Jakarta Sans**: For the beautiful typography

## 📞 Support

If you encounter issues or have questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Try with smaller files first
4. Report issues with detailed error messages

---

**Tip**: For best results, use videos under 2 minutes for faster processing and more accurate captions.