from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
from keras.models import load_model
import os
from werkzeug.utils import secure_filename
import base64
from io import BytesIO

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load the trained model
try:
    model = load_model('dog_breed.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Class names
CLASS_NAMES = ['Scottish Deerhound', 'Maltese Dog', 'Bernese Mountain Dog']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_breed(image_array):
    """Predict dog breed from image array"""
    if model is None:
        return None, "Model not loaded"
    
    # Resize to model input size
    image_array = cv2.resize(image_array, (224, 224))
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    
    # Make prediction
    prediction = model.predict(image_array)
    breed_index = np.argmax(prediction)
    breed_name = CLASS_NAMES[breed_index]
    confidence = float(prediction[0][breed_index]) * 100
    
    return breed_name, confidence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, or GIF'}), 400
        
        # Read the image
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        
        if image is None:
            return jsonify({'error': 'Could not read image'}), 400
        
        # Make prediction
        breed_name, confidence = predict_breed(image)
        
        if breed_name is None:
            return jsonify({'error': confidence}), 500
        
        # Convert image to base64 for display
        _, buffer = cv2.imencode('.png', image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'breed': breed_name,
            'confidence': round(confidence, 2),
            'image': f'data:image/png;base64,{img_base64}'
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error during prediction: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
