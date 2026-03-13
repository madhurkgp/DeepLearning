import streamlit as st
import cv2
import numpy as np
from PIL import Image
import logging as log
import datetime as dt
import time

# Configure page
st.set_page_config(
    page_title="Face Detection App",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .info-message {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize face detection
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log', level=log.INFO)

# Streamlit begins

# Enhanced Header
st.markdown('<h1 class="main-header">🎭 Face Detection App</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Real-time face detection using OpenCV and Streamlit</p>', unsafe_allow_html=True)

# Stats Dashboard
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Technology", "OpenCV")
with col2:
    st.metric("Algorithm", "Haar Cascade")
with col3:
    st.metric("Interface", "Web App")

st.markdown("---")

# Enhanced Sidebar
st.sidebar.markdown("## ⚙️ Settings")

# Detection Parameters
st.sidebar.markdown("### Detection Parameters")
scale_factor = st.sidebar.slider("Scale Factor", 1.1, 2.0, 1.1, 0.1)
min_neighbors = st.sidebar.slider("Min Neighbors", 3, 10, 5)
min_size = st.sidebar.slider("Min Face Size", 20, 100, 30)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Detection Info")
detection_info = st.sidebar.empty()

# App Info
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.info("This app uses Haar Cascade classifiers to detect faces in images and real-time video streams.")

# Main App Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📤 Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], 
                                   help="Upload an image to detect faces")

with col2:
    st.markdown("### 📹 Live Camera")
    use_webcam = st.checkbox("Use Webcam", help="Enable real-time face detection")

if uploaded_file is not None:
    # Process uploaded image
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    
    # Convert to OpenCV format
    frame = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces with user parameters
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=(min_size, min_size)
    )
    
    # Draw enhanced rectangles around faces
    for (x, y, w, h) in faces:
        # Draw rectangle with rounded corners effect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # Add label
        cv2.putText(frame, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Convert back to RGB for display
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Display results
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.image(frame_rgb, caption=f"🎯 Detected {len(faces)} face(s)", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update sidebar info
    detection_info.metric("Faces Found", len(faces))
    
    # Show detection stats
    if len(faces) > 0:
        st.markdown(f'<div class="success-message">✅ Successfully detected {len(faces)} face(s)!</div>', unsafe_allow_html=True)
        log.info(f"faces: {len(faces)} at {dt.datetime.now()}")
    else:
        st.markdown('<div class="info-message">ℹ️ No faces detected. Try adjusting parameters or use a clearer image.</div>', unsafe_allow_html=True)

elif use_webcam:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 📹 Live Face Detection")
    st.write("Click 'Start Webcam' to begin real-time face detection")
    
    col_start, col_stop = st.columns(2)
    
    with col_start:
        if st.button("🚀 Start Webcam", type="primary"):
            # Initialize webcam
            video_capture = cv2.VideoCapture(0)
            
            if not video_capture.isOpened():
                st.markdown('<div class="error-message">❌ Unable to load camera. Please make sure your webcam is connected.</div>', unsafe_allow_html=True)
            else:
                stframe = st.empty()
                status_text = st.empty()
                face_count_text = st.empty()
                
                status_text.markdown('<div class="success-message">📹 Webcam is running... Click "Stop Webcam" to stop.</div>', unsafe_allow_html=True)
                
                while video_capture.isOpened():
                    ret, frame = video_capture.read()
                    
                    if ret:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        
                        faces = faceCascade.detectMultiScale(
                            gray,
                            scaleFactor=scale_factor,
                            minNeighbors=min_neighbors,
                            minSize=(min_size, min_size)
                        )
                        
                        # Draw enhanced rectangles around faces
                        for (x, y, w, h) in faces:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            cv2.putText(frame, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        
                        # Convert to RGB for display
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        # Display the frame
                        stframe.image(frame_rgb, channels="RGB", use_column_width=True)
                        
                        # Update face count
                        face_count_text.metric("Faces Detected", len(faces))
                        
                        # Update sidebar info
                        detection_info.metric("Faces Found", len(faces))
                        
                        # Log detection
                        if len(faces) > 0:
                            log.info(f"faces: {len(faces)} at {dt.datetime.now()}")
                        
                        # Small delay to prevent excessive CPU usage
                        time.sleep(0.05)
                    else:
                        st.markdown('<div class="error-message">❌ Failed to capture frame from camera</div>', unsafe_allow_html=True)
                        break
                
                # Release the capture
                video_capture.release()
                status_text.markdown('<div class="info-message">⏹️ Webcam stopped</div>', unsafe_allow_html=True)
    
    with col_stop:
        if st.button("⏹️ Stop Webcam", type="secondary"):
            # This will be handled by the streamlit session state
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="info-message">📷 Please upload an image or enable webcam to start face detection.</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("### 📚 Learn More")

expander = st.expander("🔍 About Haar Cascade Detection")
with expander:
    st.markdown("""
    **Haar Cascade classifiers** are machine learning object detection algorithms that can identify objects in images and video.
    
    **How it works:**
    - Uses Haar-like features to detect objects
    - Trained on positive and negative images
    - Efficient real-time detection
    - 
    **Applications:**
    - Face detection
    - Eye detection
    - Smile detection
    - Full body detection
    """)
    
# Footer info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Framework", "Streamlit")
with col2:
    st.metric("Library", "OpenCV")
with col3:
    st.metric("Model", "Haar Cascade")