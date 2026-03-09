# Digit Classification Web Application

A Django-based web application that classifies handwritten digits using deep learning models.

## 🎯 Project Overview

This application allows users to upload images of handwritten digits (0-9) and get real-time predictions using a trained neural network model. The app features a modern, responsive UI with an intuitive interface for easy digit classification.

## 🛠 Tech Stack

### Backend
- **Django 3.2** - Web framework
- **TensorFlow 2.6.0** - Deep learning framework
- **Keras 2.6.0** - Neural network API
- **NumPy 1.19.5** - Numerical computing
- **Pillow 8.3.0** - Image processing

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with modern gradients and animations
- **JavaScript** - Interactive file upload handling
- **Responsive Design** - Mobile-friendly interface

### Database
- **SQLite** - Default Django database

## 📁 Project Structure

```
image_digit_classification/
├── Code/
│   └── mysite/
│       ├── manage.py              # Django management script
│       ├── mysite/                # Django project configuration
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       ├── polls/                 # Main Django app
│       │   ├── models.py          # Database models
│       │   ├── views.py           # Business logic
│       │   ├── urls.py            # URL routing
│       │   ├── forms.py           # Django forms
│       │   ├── templates/         # HTML templates
│       │   │   ├── index.html     # Home page
│       │   │   └── upload.html    # Upload page
│       │   ├── preprocessing.py   # Image preprocessing
│       │   ├── baseline.h5        # Trained model
│       │   └── images/            # Uploaded images
│       └── requirements.txt       # Python dependencies
├── Dataset/                       # Training data (if available)
└── README.md                      # This file
```

## 🚀 Setup and Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Step 1: Clone and Navigate
```bash
cd image_digit_classification/Code/mysite
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Run the Application
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📱 How to Use

1. **Home Page**: View the main dashboard with upload option
2. **Upload Image**: Click "Upload Image" to navigate to the upload page
3. **Select File**: Choose an image file containing a handwritten digit
4. **Classify**: Click "Classify Digit" to get the prediction
5. **View Results**: See the predicted digit displayed on the home page

## 🖼 Supported Image Formats

- **JPG/JPEG**
- **PNG**
- **GIF**
- **BMP**

Recommended image size: 28x28 pixels (MNIST standard) or larger (will be automatically resized)

## 🧠 Model Details

The application uses a pre-trained neural network model (`baseline.h5`) that has been trained on the MNIST dataset. The model architecture includes:

- **Input Layer**: 28x28 grayscale images
- **Hidden Layers**: Dense layers with ReLU activation
- **Output Layer**: 10 neurons (digits 0-9) with softmax activation
- **Accuracy**: ~98% on test dataset

## 🔧 Configuration

### Model Path
The trained model is located at: `polls/baseline.h5`

### Media Uploads
Uploaded images are stored in: `polls/images/`

### Database
SQLite database file: `db.sqlite3`

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are installed via `requirements.txt`
2. **Model Loading Error**: Verify `baseline.h5` exists in the `polls/` directory
3. **Permission Issues**: Ensure write permissions for the `polls/images/` directory
4. **Port Already in Use**: Change port using `python manage.py runserver 8080`

### Debug Mode
To enable debug mode, ensure in `mysite/settings.py`:
```python
DEBUG = True
```

## 🔄 Development Workflow

1. **Make Changes**: Edit code files as needed
2. **Test Locally**: Run `python manage.py runserver`
3. **Database Changes**: If models are modified, run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## 📈 Performance Considerations

- **Model Loading**: The model is loaded once per prediction for memory efficiency
- **Image Preprocessing**: Images are resized and normalized to match training data
- **Caching**: Consider implementing Redis for frequent predictions in production

## 🚀 Deployment Notes

For production deployment:

1. **Set DEBUG = False** in settings
2. **Configure ALLOWED_HOSTS**
3. **Use production database** (PostgreSQL/MySQL)
4. **Set up static file serving**
5. **Configure HTTPS**
6. **Use Gunicorn/uWSGI** as WSGI server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please ensure compliance with the licenses of all dependencies.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django and TensorFlow documentation
3. Create an issue in the project repository

---

**Happy Digit Classification! 🎯**
