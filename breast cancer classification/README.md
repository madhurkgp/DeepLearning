# Breast Cancer Detection System

An AI-powered web application for breast cancer histopathology image classification using deep learning.

## Features

- **Modern UI**: Clean, responsive design with gradient backgrounds and animations
- **AI-Powered Analysis**: Uses DenseNet201 model trained on histopathology images
- **Real-time Prediction**: Instant analysis of uploaded images
- **Professional Interface**: User-friendly upload and results display
- **Mobile Responsive**: Works on all device sizes

## Dataset

- **Source**: Breast Cancer Histopathological Database (BreakHis)
- **Classes**: Benign (114 images) and Malignant (127 images)
- **Format**: PNG images
- **Resolution**: 224x224 pixels (optimized for model)

## Model Architecture

- **Base Model**: DenseNet201 (pre-trained on ImageNet)
- **Input Size**: 224x224 RGB images
- **Output**: Binary classification (Benign/Malignant)
- **Accuracy**: ~95% on training data

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone/Download the project**
   ```bash
   cd "breast cancer classification/Code/mysite"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`

## Usage

1. **Upload Image**: Click "Choose Image" to upload a histopathology PNG image
2. **Analyze**: Click "Analyze Image" to process the image
3. **View Results**: Get instant classification (Benign/Malignant)
4. **Upload More**: Click back to analyze additional images

## Project Structure

```
breast cancer classification/
├── benign/                    # Benign histopathology images (114 files)
├── malign/                    # Malignant histopathology images (127 files)
├── Code/
│   ├── Breast Cancer.ipynb    # Training notebook (updated for local paths)
│   └── mysite/               # Django web application
│       ├── manage.py          # Django management script
│       ├── requirements.txt    # Python dependencies
│       ├── mysite/           # Django project settings
│       └── polls/            # Main application
│           ├── views.py       # Prediction logic
│           ├── models.py      # Database models
│           ├── forms.py       # Upload forms
│           ├── templates/     # HTML templates
│           └── breast-cancer-model.h5  # Trained model (220MB)
└── README.md                 # This file
```

## Model Training

To retrain the model:

1. Open `Breast Cancer.ipynb` in Jupyter
2. Run all cells to train on the local dataset
3. Model and preprocessing pipeline will be saved automatically

## Technical Details

### Frontend Features
- Modern gradient design with animations
- Drag-and-drop file upload
- Loading indicators
- Responsive layout
- Professional medical interface

### Backend Features
- Django REST API
- TensorFlow/Keras model integration
- Image preprocessing pipeline
- File upload handling
- Database storage for uploads

### Model Pipeline
1. **Preprocessing**: Image resizing and normalization
2. **Prediction**: DenseNet201 feature extraction + classification
3. **Results**: Binary output with confidence scores

## Dependencies

- **Django 3.2.0**: Web framework
- **TensorFlow 2.8.0**: Deep learning framework
- **Keras 2.8.0**: Neural network API
- **OpenCV 4.5.5.64**: Image processing
- **Pillow 9.0.0**: Image manipulation
- **NumPy 1.22.0**: Numerical computing
- **Scikit-learn 1.1.0**: Machine learning utilities
- **Pandas 1.4.0**: Data manipulation

## Notes

- The model is trained on a small dataset (241 images total)
- For production use, consider training on the full BreakHis dataset (4GB)
- GPU acceleration is recommended for faster predictions
- Always consult healthcare professionals for medical decisions

## Troubleshooting

**Common Issues:**

1. **Numpy Compatibility**: Ensure numpy 1.22.0 is installed
2. **Missing Model**: The trained model is included in `polls/breast-cancer-model.h5`
3. **Port Already in Use**: Change port with `python manage.py runserver 8080`
4. **Import Errors**: Run `pip install -r requirements.txt` again

**Performance Tips:**

- Use GPU for faster predictions
- Optimize image sizes before upload
- Consider model quantization for deployment

## License

This project is for educational and research purposes. The BreakHis dataset has its own usage terms that should be followed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Contact

For questions or issues, please create an issue in the repository.
