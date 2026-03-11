# Advertisement Classification System

A Django-based web application that classifies advertisements into different categories using a deep learning model.

## Project Overview

This project uses a trained LSTM neural network to classify advertisements based on their title and description into one of the following categories:
- Art and Music
- Food
- History
- Manufacturing
- Science and Technology
- Travel

## Project Structure

```
advertisement_classification/
├── Code/
│   ├── Video_classification.ipynb    # Jupyter notebook with model training code
│   └── mysite/                       # Django web application
│       ├── manage.py                 # Django management script
│       ├── requirements.txt          # Python dependencies
│       ├── mysite/                   # Django project configuration
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── ...
│       └── polls/                    # Django app for classification
│           ├── views.py              # Main view logic
│           ├── models.py
│           ├── templates/
│           │   └── index.html        # Web interface
│           ├── video_classification-model.h5    # Trained model
│           └── video_classification-tokenizer.pkl # Tokenizer
└── Dataset/
    └── Videos_data.csv               # Training dataset
```

## Features

- **Web Interface**: User-friendly form for inputting advertisement title and description
- **Real-time Classification**: Instant classification using pre-trained deep learning model
- **Multiple Categories**: Supports 6 different advertisement categories
- **Responsive Design**: Clean and modern web interface

## Technology Stack

- **Backend**: Django 3.2
- **Machine Learning**: TensorFlow 2.6.0, Keras 2.6.0
- **Natural Language Processing**: NLTK
- **Frontend**: HTML, CSS
- **Data Processing**: Pandas, NumPy

## Installation and Setup

### Prerequisites

- Python 3.7+
- pip package manager

### Step 1: Clone/Download the Project

Ensure you have the project folder in your desired location.

### Step 2: Install Dependencies

Navigate to the project directory and install the required packages:

```bash
cd advertisement_classification/Code/mysite
pip install -r requirements.txt
```

### Step 3: Download NLTK Data

Run the following Python commands to download required NLTK data:

```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
```

### Step 4: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Application

### Method 1: Using the Run Script (Recommended)

```bash
cd advertisement_classification/Code/mysite
python run_server.py
```

### Method 2: Using Django's Development Server

```bash
cd advertisement_classification/Code/mysite
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:8000/`
2. Enter the advertisement title in the first input field
3. Enter the advertisement description in the second input field
4. Click the "Submit" button
5. The system will display the predicted category for your advertisement

## Model Details

The classification model is an LSTM-based neural network trained on a dataset of video advertisements. The model processes text data using:

- **Text Preprocessing**: Lowercase conversion, stopword removal, lemmatization
- **Tokenization**: Converts text to numerical sequences
- **Padding**: Ensures uniform input length (max 50 words)
- **LSTM Architecture**: 128 units with dropout for regularization
- **Output Layer**: 6 neurons with softmax activation for multi-class classification

## Dataset

The model was trained on the `Videos_data.csv` dataset containing:
- Video titles and descriptions
- Category labels (6 classes)
- ~10,000 samples after preprocessing

## Model Performance

The trained model achieves good accuracy on the classification task with the following class distribution:
- Manufacturing: 866 samples
- Science and Technology: 849 samples
- Art and Music: 845 samples
- Travel: 816 samples
- History: 814 samples
- Food: 810 samples

## File Descriptions

### Core Files
- `views.py`: Contains the main classification logic and web interface handling
- `index.html`: Frontend template for user input and results display
- `video_classification-model.h5`: Pre-trained Keras model
- `video_classification-tokenizer.pkl`: Text tokenizer for preprocessing

### Configuration Files
- `settings.py`: Django project settings
- `urls.py`: URL routing configuration
- `requirements.txt`: Python package dependencies

### Training Code
- `Video_classification.ipynb`: Complete Jupyter notebook with data preprocessing, model training, and evaluation

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **NLTK Data Missing**: Download required NLTK data using the commands in the setup section
3. **Model Loading Error**: Ensure the model files (`video_classification-model.h5` and `video_classification-tokenizer.pkl`) are in the `polls/` directory
4. **Port Already in Use**: Change the port using `python manage.py runserver 8080`

### Dependencies

Make sure you have the following key packages installed:
- Django==3.2
- tensorflow-cpu==2.6.0
- Keras==2.6.0
- nltk
- pandas
- numpy
- scikit-learn

## Contributing

To extend or modify this project:

1. **Retrain the Model**: Use `Video_classification.ipynb` to train with new data
2. **Add New Categories**: Modify the `label_reverse()` function in `views.py`
3. **Improve UI**: Edit `index.html` for better user experience
4. **Add Features**: Extend the Django app with additional views and functionality

## License

This project is provided for educational and research purposes.

## Contact

For questions or issues regarding this project, please refer to the project documentation or create an issue in the project repository.
