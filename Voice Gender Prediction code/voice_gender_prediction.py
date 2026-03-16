#!/usr/bin/env python3
"""
Voice Gender Prediction System

This module provides functionality to predict gender from audio features
using a trained Random Forest model.
"""

import pandas as pd
import numpy as np
import pickle
import os
import logging
from typing import Optional, Union, Dict, Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceGenderPredictor:
    """
    A class for predicting gender from voice features using machine learning.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the predictor.
        
        Args:
            model_path: Path to the trained model file. If None, uses default path.
        """
        self.model = None
        self.feature_columns = [
            'sd', 'median', 'Q25', 'Q75', 'IQR', 'skew', 'sp.ent', 
            'mode', 'centroid', 'meanfun', 'minfun', 'maxfun', 
            'mindom', 'maxdom', 'modindx'
        ]
        
        if model_path:
            self.model_path = model_path
        else:
            self.model_path = os.path.join(os.path.dirname(__file__), 'voice_model.pickle')
        
        self.load_model()
    
    def load_model(self) -> bool:
        """
        Load the trained model from disk.
        
        Returns:
            bool: True if model loaded successfully, False otherwise.
        """
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"Model loaded successfully from {self.model_path}")
                return True
            else:
                logger.warning(f"Model file not found at {self.model_path}")
                return False
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def predict(self, features: Union[Dict[str, float], pd.DataFrame]) -> Optional[str]:
        """
        Predict gender from voice features.
        
        Args:
            features: Voice features as dictionary or DataFrame.
            
        Returns:
            str: Predicted gender ('male' or 'female'), or None if prediction fails.
        """
        if self.model is None:
            logger.error("No model loaded for prediction")
            return None
        
        try:
            # Convert dict to DataFrame if needed
            if isinstance(features, dict):
                # Ensure all required features are present
                for feature in self.feature_columns:
                    if feature not in features:
                        raise ValueError(f"Missing required feature: {feature}")
                
                df = pd.DataFrame([features])
            else:
                df = features
            
            # Ensure correct column order
            df = df[self.feature_columns]
            
            # Make prediction
            prediction = self.model.predict(df)
            return prediction[0] if len(prediction) > 0 else None
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return None
    
    def train_model(self, data_path: str, save_model: bool = True) -> Dict[str, Any]:
        """
        Train a new Random Forest model on voice data.
        
        Args:
            data_path: Path to the CSV dataset.
            save_model: Whether to save the trained model.
            
        Returns:
            Dict containing training metrics.
        """
        try:
            # Load data
            df = pd.read_csv(data_path)
            logger.info(f"Dataset loaded with shape: {df.shape}")
            
            # Drop unnecessary columns (as done in notebook)
            columns_to_drop = ['dfrange', 'kurt', 'sfm', 'meandom', 'meanfreq']
            existing_columns = [col for col in columns_to_drop if col in df.columns]
            df = df.drop(existing_columns, axis=1)
            
            # Prepare features and target
            X = df.drop(['label'], axis=1)
            y = df['label']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=500, 
                random_state=42
            )
            self.model.fit(X_train, y_train)
            
            # Evaluate
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
            y_pred = self.model.predict(X_test)
            
            metrics = {
                'train_accuracy': train_score,
                'test_accuracy': test_score,
                'classification_report': classification_report(y_test, y_pred),
                'feature_importance': dict(zip(X.columns, self.model.feature_importances_))
            }
            
            logger.info(f"Training completed. Test accuracy: {test_score:.2f}")
            
            # Save model if requested
            if save_model:
                self.save_model()
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error during training: {str(e)}")
            return {}
    
    def save_model(self) -> bool:
        """
        Save the trained model to disk.
        
        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            if self.model is not None:
                with open(self.model_path, 'wb') as f:
                    pickle.dump(self.model, f)
                logger.info(f"Model saved to {self.model_path}")
                return True
            else:
                logger.error("No model to save")
                return False
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False


def extract_audio_features(audio_path: str) -> Optional[Dict[str, float]]:
    """
    Extract voice features from an audio file.
    
    Note: This is a placeholder function. In a production environment,
    you would use librosa or similar library to extract actual features.
    
    Args:
        audio_path: Path to the audio file.
        
    Returns:
        Dict of extracted features, or None if extraction fails.
    """
    try:
        # This would be implemented with librosa in production
        # For now, return sample features for demonstration
        logger.warning("Audio feature extraction not implemented. Using sample features.")
        return {
            'sd': 0.064,
            'median': 0.032,
            'Q25': 0.015,
            'Q75': 0.090,
            'IQR': 0.075,
            'skew': 12.86,
            'sp.ent': 0.893,
            'mode': 0.0,
            'centroid': 0.059,
            'meanfun': 0.084,
            'minfun': 0.015,
            'maxfun': 0.276,
            'mindom': 0.007,
            'maxdom': 0.007,
            'modindx': 0.0
        }
    except Exception as e:
        logger.error(f"Error extracting features from {audio_path}: {str(e)}")
        return None


def main():
    """
    Main function for command-line usage.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Voice Gender Prediction')
    parser.add_argument('--train', type=str, help='Path to training data CSV')
    parser.add_argument('--predict', type=str, help='Path to audio file for prediction')
    parser.add_argument('--model', type=str, help='Path to model file')
    
    args = parser.parse_args()
    
    predictor = VoiceGenderPredictor(args.model)
    
    if args.train:
        print(f"Training model on {args.train}...")
        metrics = predictor.train_model(args.train)
        if metrics:
            print(f"Training completed. Test accuracy: {metrics['test_accuracy']:.2f}")
        else:
            print("Training failed")
    
    elif args.predict:
        print(f"Predicting gender for {args.predict}...")
        features = extract_audio_features(args.predict)
        if features:
            prediction = predictor.predict(features)
            if prediction:
                print(f"Predicted gender: {prediction}")
            else:
                print("Prediction failed")
        else:
            print("Feature extraction failed")
    
    else:
        print("Please specify --train or --predict")


if __name__ == "__main__":
    main()
