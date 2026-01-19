#Library imports
import numpy as np
import cv2
from keras.models import load_model
from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

#Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

#Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

#Loading the Model
model = load_model('plant_disease.h5')

#Name of Classes
CLASS_NAMES = ['Corn-Common_rust', 'Potato-Early_blight', 'Tomato-Bacterial_spot']

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image
        try:
            # Read and process image
            image = cv2.imread(filepath)
            if image is None:
                return render_template('index.html', error="Invalid image file")
            
            # Display image info
            original_shape = image.shape
            
            # Resize and preprocess
            processed_image = cv2.resize(image, (256, 256))
            processed_image = processed_image.reshape(1, 256, 256, 3)
            
            # Make prediction
            prediction = model.predict(processed_image)
            result = CLASS_NAMES[np.argmax(prediction)]
            
            # Format result
            plant_type = result.split('-')[0]
            disease = result.split('-')[1]
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return render_template('result.html', 
                                 plant_type=plant_type, 
                                 disease=disease,
                                 filename=filename,
                                 original_shape=original_shape)
        
        except Exception as e:
            # Clean up uploaded file if it exists
            if os.path.exists(filepath):
                os.remove(filepath)
            return render_template('index.html', error=f"Error processing image: {str(e)}")
    
    return render_template('index.html', error="Invalid file type. Please upload JPG, JPEG, or PNG files.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
