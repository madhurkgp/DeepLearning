# Dog Breed Prediction Web App

A Flask-based web application for predicting dog breeds from images using a trained deep learning model.

## Project Structure

```
Dog Breed Prediction Streamlit App/
├── app.py                    # Flask main application
├── dog_breed.h5             # Pre-trained model weights
├── requirements_flask.txt   # Python dependencies
├── templates/
│   └── index.html          # Frontend HTML/CSS/JavaScript
└── README.md               # This file
```

## Features

- 🐕 Predict dog breed from image uploads
- 🎨 Beautiful and responsive UI
- 📱 Mobile-friendly design
- 🖼️ Drag and drop image upload
- 📊 Confidence percentage display
- ⚡ Real-time predictions

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd "Dog Breed Prediction Streamlit App"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_flask.txt
   ```

4. **Ensure the model file exists**
   - Place `dog_breed.h5` in the same directory as `app.py`

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Access the web app**
   - Open your browser and go to: `http://localhost:5000`
   - The app will be running on your local machine

3. **Using the app**
   - Click on the upload area or drag and drop an image
   - Click the "Predict" button
   - Wait for the prediction result
   - View the breed name and confidence percentage

## API Endpoints

### 1. GET `/`
Returns the main HTML page

### 2. POST `/predict`
Accepts an image file and returns breed prediction
- **Request**: Multipart form data with file
- **Response**: JSON with breed name, confidence, and base64 image

```json
{
    "success": true,
    "breed": "Scottish Deerhound",
    "confidence": 95.23,
    "image": "data:image/png;base64,..."
}
```

### 3. GET `/health`
Health check endpoint
- **Response**: Model status

```json
{
    "status": "healthy",
    "model_loaded": true
}
```

## Supported Dog Breeds

The model is trained to predict:
- Scottish Deerhound
- Maltese Dog
- Bernese Mountain Dog

## Configuration

### To change the port
Edit `app.py` and modify:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### To add more dog breeds
1. Update the `CLASS_NAMES` list in `app.py`
2. Retrain your model with the new breeds
3. Update `dog_breed.h5` with the new model

## Troubleshooting

### Model not loading
- Ensure `dog_breed.h5` is in the correct directory
- Check the file permissions
- Verify the file is not corrupted

### Port already in use
```bash
# Find and kill the process using port 5000
# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Image upload fails
- Check file size (max 16MB)
- Ensure image format is supported (PNG, JPG, JPEG, GIF)
- Check browser console for errors

## Deployment

### Local Network Access
To access from other devices on your network:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
Then access via `http://<your-ip>:5000`

### Production Deployment (Using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **ML Model**: Keras/TensorFlow
- **Image Processing**: OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **HTTP**: RESTful API

## Performance Notes

- Model prediction takes 2-5 seconds depending on hardware
- Images are automatically resized to 224x224 pixels for the model
- Maximum file size: 16MB

## Future Enhancements

- [ ] Add support for more dog breeds
- [ ] Implement image caching
- [ ] Add prediction history
- [ ] Improve model accuracy with newer training data
- [ ] Add Docker support
- [ ] Implement user authentication

## License

This project is for educational purposes.

## Support

For issues or questions, please check the error messages in the browser console and Flask terminal output.
