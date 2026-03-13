# Face Detection Application

A real-time face detection web application built with Streamlit and OpenCV using Haar Cascade classifiers.

## 🚀 Features

- **Real-time Face Detection**: Detect faces in real-time using your webcam
- **Image Upload**: Upload and analyze images for face detection
- **Interactive Web Interface**: User-friendly Streamlit interface
- **Educational Content**: Learn about Haar Cascade classifiers and face detection algorithms
- **Logging**: Automatic logging of detection events

## 🛠️ Technologies Used

### Core Libraries
- **Streamlit** (>=1.28.0): Web framework for building interactive ML applications
- **OpenCV** (>=4.8.0): Computer vision library for face detection
- **NumPy** (>=1.24.0): Numerical computing for image processing
- **Pillow** (>=9.5.0): Image processing and display

### Algorithm
- **Haar Cascade Classifier**: Machine learning-based object detection method proposed by Paul Viola and Michael Jones
- **Pre-trained Model**: Uses `haarcascade_frontalface_default.xml` for frontal face detection

## 📋 Prerequisites

- Python 3.7 or higher
- Webcam (for real-time detection)
- Internet connection (for installing dependencies)

## 🚀 Installation and Setup

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd face_recognition/Code

# Or download and extract the files
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🎯 How to Run

### Method 1: Direct Command
```bash
streamlit run Streamlit_cam.py
```

### Method 2: Using Python
```bash
python -m streamlit run Streamlit_cam.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Image Upload Detection
1. Click "Choose an image..." to upload a JPG, JPEG, or PNG file
2. The app will automatically detect faces and draw green rectangles around them
3. View the number of faces detected in the caption

### 2. Real-time Webcam Detection
1. Check the "Use Webcam" checkbox
2. Click "Start Webcam" to begin real-time face detection
3. Allow browser camera permissions when prompted
4. Click "Stop Webcam" to stop the detection
5. Press 'Q' on your keyboard as an alternative way to stop

### 3. Educational Content
- Browse the sidebar to learn about Haar Cascade classifiers
- Read the step-by-step explanation of the face detection process
- Understand the parameters and algorithms used

## 🔧 Technical Details

### Face Detection Parameters
- **scaleFactor**: 1.1 (10% image size reduction at each scale)
- **minNeighbors**: 5 (minimum neighboring rectangles to retain detection)
- **minSize**: (30, 30) pixels (minimum face size to detect)

### Haar Cascade Process
1. **Grayscale Conversion**: Images converted to grayscale for computational efficiency
2. **Feature Detection**: Haar-like features applied to detect facial patterns
3. **Multi-scale Detection**: Image pyramid for detecting faces at different sizes
4. **Rectangle Drawing**: Green rectangles drawn around detected faces

## 📁 Project Structure

```
face_recognition/
└── Code/
    ├── Streamlit_cam.py              # Main application file
    ├── haarcascade_frontalface_default.xml  # Pre-trained face detection model
    ├── requirements.txt               # Python dependencies
    └── README.md                     # This documentation file
```

## 🐛 Troubleshooting

### Common Issues

**Camera Not Found**
- Ensure your webcam is properly connected
- Check if other applications are using the camera
- Restart the application after connecting the camera

**Dependencies Installation Errors**
- Upgrade pip: `pip install --upgrade pip`
- Use virtual environment to avoid conflicts
- Install packages individually if requirements.txt fails

**Application Not Loading**
- Check if port 8501 is available
- Try running on a different port: `streamlit run Streamlit_cam.py --server.port 8502`
- Check Python and Streamlit versions compatibility

**Face Detection Not Working**
- Ensure adequate lighting conditions
- Check if faces are clearly visible and not obstructed
- Try with different image angles and distances

## 📝 Logging

The application automatically logs face detection events to `webcam.log`:
- Timestamp of detection
- Number of faces detected
- Error messages (if any)

## 🔒 Privacy and Security

- No images or video data are stored on disk
- Processing happens in real-time in memory
- Webcam access requires explicit user permission
- Logs contain only metadata (timestamps and face counts)

## 🤝 Contributing

Feel free to contribute improvements:
- Add new detection features (eye detection, smile detection)
- Improve UI/UX
- Add support for video files
- Enhance performance optimization

## 📄 License

This project is for educational purposes. Please refer to the licenses of the respective libraries used.

## 🙏 Acknowledgments

- OpenCV team for the computer vision library
- Streamlit team for the web framework
- Paul Viola and Michael Jones for the Haar Cascade algorithm

---

**Happy Face Detecting! 🎭**
