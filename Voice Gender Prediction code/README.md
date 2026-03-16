# Voice Gender Prediction System

A machine learning system that predicts gender from voice features using a Random Forest classifier. This project includes both a standalone Python script and a Django web application for easy deployment and use.

## 🎯 Project Overview

The Voice Gender Prediction system analyzes audio features extracted from voice recordings to classify whether the speaker is male or female. The system achieves approximately 98% accuracy on test data using a Random Forest model trained on 15 key acoustic features.

## 📊 Features

- **High Accuracy**: ~98% test accuracy using Random Forest classifier
- **Multiple Input Methods**: Support for both manual feature input and audio file upload
- **Web Interface**: Django-based web application for easy interaction
- **API Endpoints**: RESTful API for programmatic access
- **Robust Error Handling**: Comprehensive validation and error reporting
- **Audio Feature Extraction**: Automatic feature extraction from audio files using librosa

## 🛠️ Technology Stack

### Machine Learning
- **scikit-learn**: Random Forest classifier and data preprocessing
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **scipy**: Statistical operations

### Audio Processing
- **librosa**: Audio feature extraction and analysis

### Web Framework
- **Django**: Web application framework
- **gunicorn**: WSGI HTTP Server

## 📁 Project Structure

```
Voice Gender Prediction code/
├── voice_gender_prediction.py      # Main ML prediction script
├── audio_feature_extractor.py      # Audio feature extraction module
├── gender_voice_dataset.csv        # Training dataset
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── GenderPrediction.ipynb         # Original Jupyter notebook (reference)
└── mysite/                        # Django web application
    ├── manage.py
    ├── requirements.txt
    ├── mysite/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── polls/
        ├── views.py               # Main application logic
        ├── urls.py
        ├── models.py
        └── voice_model.pickle     # Trained model
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project** to your local machine

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Train the model** (optional - pre-trained model included):
```bash
python voice_gender_prediction.py --train gender_voice_dataset.csv
```

## 📖 Usage

### 1. Standalone Python Script

#### Predict from Manual Features:
```bash
python voice_gender_prediction.py --predict path/to/audio.wav
```

#### Train New Model:
```bash
python voice_gender_prediction.py --train gender_voice_dataset.csv
```

#### Programmatic Usage:
```python
from voice_gender_prediction import VoiceGenderPredictor

# Initialize predictor
predictor = VoiceGenderPredictor()

# Predict from features
features = {
    'sd': 0.064, 'median': 0.032, 'Q25': 0.015, 'Q75': 0.090,
    'IQR': 0.075, 'skew': 12.86, 'sp.ent': 0.893, 'mode': 0.0,
    'centroid': 0.059, 'meanfun': 0.084, 'minfun': 0.015,
    'maxfun': 0.276, 'mindom': 0.007, 'maxdom': 0.007, 'modindx': 0.0
}

result = predictor.predict(features)
print(f"Predicted gender: {result}")
```

### 2. Audio Feature Extraction

```python
from audio_feature_extractor import AudioFeatureExtractor

extractor = AudioFeatureExtractor()
features = extractor.extract_features("path/to/audio.wav")
print(f"Extracted features: {features}")
```

### 3. Django Web Application

#### Start the development server:
```bash
cd mysite
python manage.py runserver
```

#### Access the web interface:
- Open your browser and navigate to `http://localhost:8000/`
- Use the web form to input voice features manually
- Or upload an audio file for automatic feature extraction

#### API Usage:
```bash
# POST request to API endpoint
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "sd": 0.064, "median": 0.032, "Q25": 0.015, "Q75": 0.090,
      "IQR": 0.075, "skew": 12.86, "sp.ent": 0.893, "mode": 0.0,
      "centroid": 0.059, "meanfun": 0.084, "minfun": 0.015,
      "maxfun": 0.276, "mindom": 0.007, "maxdom": 0.007, "modindx": 0.0
    }
  }'
```

## 🧪 Model Details

### Features Used
The model uses 15 acoustic features extracted from voice recordings:

1. **sd** - Standard deviation of frequency
2. **median** - Median frequency
3. **Q25** - First quantile (25th percentile)
4. **Q75** - Third quantile (75th percentile)
5. **IQR** - Interquartile range
6. **skew** - Skewness of frequency distribution
7. **sp.ent** - Spectral entropy
8. **mode** - Mode frequency
9. **centroid** - Frequency centroid
10. **meanfun** - Mean fundamental frequency
11. **minfun** - Minimum fundamental frequency
12. **maxfun** - Maximum fundamental frequency
13. **mindom** - Minimum dominant frequency
14. **maxdom** - Maximum dominant frequency
15. **modindx** - Modulation index

### Model Performance
- **Training Accuracy**: 100%
- **Test Accuracy**: ~98%
- **Algorithm**: Random Forest (500 trees)
- **Cross-validation**: 80/20 train-test split

### Feature Importance
The most important features for gender prediction are:
1. **meanfun** - Mean fundamental frequency (most discriminative)
2. **IQR** - Interquartile range
3. **Q25** - First quantile
4. **sp.ent** - Spectral entropy
5. **centroid** - Frequency centroid

## 🔧 Configuration

### Model Path
By default, the system looks for the model at `voice_model.pickle`. You can specify a custom path:

```python
predictor = VoiceGenderPredictor(model_path="path/to/your/model.pickle")
```

### Audio Processing Settings
Configure audio processing parameters:

```python
extractor = AudioFeatureExtractor(sample_rate=22050)  # Default sample rate
```

## 🧹 Testing

Run the test suite to verify functionality:

```bash
# Run basic functionality tests
python -m pytest tests/

# Run Django tests
cd mysite
python manage.py test
```

### Test Coverage
- Model loading and prediction
- Feature extraction from audio files
- Error handling for invalid inputs
- API endpoint functionality
- Web form processing

## 🚨 Error Handling

The system includes comprehensive error handling for:

- **Invalid audio formats**: Only WAV and MP3 files are supported
- **Missing features**: Validates all required features are present
- **Invalid numeric values**: Checks for reasonable ranges
- **Model loading errors**: Graceful handling of missing/corrupted models
- **File not found**: Clear error messages for missing files

## 📝 API Reference

### Predict Gender
**Endpoint**: `POST /api/predict/`

**Request Body**:
```json
{
  "features": {
    "sd": 0.064,
    "median": 0.032,
    "Q25": 0.015,
    "Q75": 0.090,
    "IQR": 0.075,
    "skew": 12.86,
    "sp.ent": 0.893,
    "mode": 0.0,
    "centroid": 0.059,
    "meanfun": 0.084,
    "minfun": 0.015,
    "maxfun": 0.276,
    "mindom": 0.007,
    "maxdom": 0.007,
    "modindx": 0.0
  }
}
```

**Response**:
```json
{
  "prediction": "male"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid JSON or missing features
- `500 Internal Server Error`: Model prediction failed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset source: [Voice Gender Dataset](https://www.kaggle.com/datasets/primaryobjects/voicegender)
- Audio processing: [librosa](https://librosa.org/)
- Machine learning: [scikit-learn](https://scikit-learn.org/)

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the repository
- Contact the development team

---

**Note**: This system is designed for educational and research purposes. Performance may vary with different audio quality, recording conditions, and demographic groups.
