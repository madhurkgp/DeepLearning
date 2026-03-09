from django.shortcuts import render, redirect
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import numpy as np
import pickle
import os
from .sustain import tokenizer


def handler(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        desc = request.POST.get('desc', '').strip()
        
        # Validate input
        if not title or not desc:
            return render(request, "index.html", {'response': 'Please enter both title and description'})
        
        try:
            result = predict(title, desc)
            fina = label_reverse(result[0])
            print(f"Classification result: {fina}")
        except Exception as e:
            print(f"Handler error: {str(e)}")
            fina = 'Error occurred during classification'
    else:
        fina = None
    return render(request, "index.html", {'response': fina})


def predict(title, desc):
    try:
        # Max number of words in each complaint.
        MAX_SEQUENCE_LENGTH = 50
        data_for_lstms = []
        data_for_lstms.append(' '.join([title, desc]))
        
        # Convert the data to padded sequences
        X = tokenizer.texts_to_sequences(data_for_lstms)
        X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)
        
        # Load model with error handling
        model_path = 'polls/video_classification-model.h5'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        model = load_model(model_path, compile=False)
        
        # Make prediction
        predict_x = model.predict(X, verbose=0)
        classes_x = np.argmax(predict_x, axis=1)
        return classes_x
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        # Return a default category in case of error
        return np.array([0])  # Default to 'art and music'


def label_reverse(result):
    if result == 0:
        return 'art and music'
    elif result == 1:
        return 'food'
    if result == 2:
        return 'history'
    if result == 3:
        return 'manufacturing'
    if result == 4:
        return 'science and technology'
    else:
        return 'travel'
