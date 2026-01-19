# Plant Disease Detection Flask App

A minimalistic Flask web application for detecting plant diseases using deep learning.

## Features

- Clean, minimalistic user interface
- Supports JPG, JPEG, and PNG image formats
- Real-time plant disease prediction
- Error handling and validation
- Responsive design

## Supported Diseases

- Corn Common Rust
- Potato Early Blight  
- Tomato Bacterial Spot

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python main_app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Click "Choose Image File" to select a plant leaf image
2. Click "Predict Disease" to analyze the image
3. View the results and click "Analyze Another Image" to try again

## File Structure

```
Plant_Disease/
├── main_app.py              # Flask application
├── plant_disease.h5         # Trained model
├── requirements.txt         # Python dependencies
├── templates/
│   ├── index.html          # Upload page
│   └── result.html         # Results page
└── uploads/                # Temporary upload directory
```

## Dependencies

- Flask 2.3.3
- Keras 2.4.3
- NumPy 1.18.5
- OpenCV 4.4.0.46
- Werkzeug 2.3.7

## Notes

- The model automatically cleans up uploaded images after processing
- Maximum file size is 16MB
- Images are resized to 256x256 pixels for prediction
- The app runs on port 5000 by default
