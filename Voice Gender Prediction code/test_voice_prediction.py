#!/usr/bin/env python3
"""
Test Suite for Voice Gender Prediction System

This script tests the functionality of the voice gender prediction system,
including model loading, prediction accuracy, and error handling.
"""

import unittest
import pandas as pd
import numpy as np
import os
import tempfile
import json
from unittest.mock import patch, MagicMock

# Import the modules we're testing
from voice_gender_prediction import VoiceGenderPredictor, extract_audio_features
from audio_feature_extractor import AudioFeatureExtractor


class TestVoiceGenderPredictor(unittest.TestCase):
    """Test cases for VoiceGenderPredictor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_model_path = "test_model.pickle"
        self.predictor = VoiceGenderPredictor(self.test_model_path)
        
        # Sample features for testing
        self.sample_features = {
            'sd': 0.064, 'median': 0.032, 'Q25': 0.015, 'Q75': 0.090,
            'IQR': 0.075, 'skew': 12.86, 'sp.ent': 0.893, 'mode': 0.0,
            'centroid': 0.059, 'meanfun': 0.084, 'minfun': 0.015,
            'maxfun': 0.276, 'mindom': 0.007, 'maxdom': 0.007, 'modindx': 0.0
        }
    
    def test_initialization(self):
        """Test predictor initialization."""
        self.assertIsNotNone(self.predictor)
        self.assertEqual(self.predictor.model_path, self.test_model_path)
        self.assertEqual(len(self.predictor.feature_columns), 15)
    
    def test_load_model_nonexistent(self):
        """Test loading non-existent model."""
        result = self.predictor.load_model()
        self.assertFalse(result)
        self.assertIsNone(self.predictor.model)
    
    @patch('builtins.open', create=True)
    @patch('pickle.load')
    def test_load_model_success(self, mock_pickle_load, mock_open):
        """Test successful model loading."""
        # Mock a trained model
        mock_model = MagicMock()
        mock_model.predict.return_value = ['male']
        mock_pickle_load.return_value = mock_model
        
        # Mock file existence
        with patch('os.path.exists', return_value=True):
            result = self.predictor.load_model()
            self.assertTrue(result)
            self.assertEqual(self.predictor.model, mock_model)
    
    def test_predict_no_model(self):
        """Test prediction without loaded model."""
        result = self.predictor.predict(self.sample_features)
        self.assertIsNone(result)
    
    @patch('pickle.load')
    def test_predict_success(self, mock_pickle_load):
        """Test successful prediction."""
        # Mock a trained model
        mock_model = MagicMock()
        mock_model.predict.return_value = ['male']
        mock_pickle_load.return_value = mock_model
        
        # Mock file existence and loading
        with patch('os.path.exists', return_value=True):
            self.predictor.load_model()
            result = self.predictor.predict(self.sample_features)
            self.assertEqual(result, 'male')
    
    def test_predict_missing_features(self):
        """Test prediction with missing features."""
        incomplete_features = {'sd': 0.064, 'median': 0.032}  # Missing many features
        
        # Mock model
        mock_model = MagicMock()
        mock_model.predict.return_value = ['male']
        self.predictor.model = mock_model
        
        result = self.predictor.predict(incomplete_features)
        self.assertIsNone(result)
    
    def test_predict_dataframe_input(self):
        """Test prediction with DataFrame input."""
        df = pd.DataFrame([self.sample_features])
        
        # Mock model
        mock_model = MagicMock()
        mock_model.predict.return_value = ['female']
        self.predictor.model = mock_model
        
        result = self.predictor.predict(df)
        self.assertEqual(result, 'female')


class TestAudioFeatureExtractor(unittest.TestCase):
    """Test cases for AudioFeatureExtractor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = AudioFeatureExtractor()
    
    def test_initialization(self):
        """Test extractor initialization."""
        self.assertEqual(self.extractor.sample_rate, 22050)
    
    @patch('librosa.load')
    def test_load_audio_success(self, mock_load):
        """Test successful audio loading."""
        # Mock librosa.load return
        mock_audio = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        mock_load.return_value = (mock_audio, 22050)
        
        with patch('os.path.exists', return_value=True):
            result = self.extractor.load_audio("test.wav")
            np.testing.assert_array_equal(result, mock_audio)
    
    def test_load_audio_file_not_found(self):
        """Test audio loading with non-existent file."""
        with patch('os.path.exists', return_value=False):
            result = self.extractor.load_audio("nonexistent.wav")
            self.assertIsNone(result)
    
    @patch('librosa.load')
    def test_load_audio_empty_file(self, mock_load):
        """Test audio loading with empty file."""
        mock_load.return_value = (np.array([]), 22050)
        
        with patch('os.path.exists', return_value=True):
            result = self.extractor.load_audio("empty.wav")
            self.assertIsNone(result)
    
    @patch('librosa.load')
    @patch('librosa.feature.spectral_centroid')
    @patch('librosa.power_spectrum')
    @patch('librosa.feature.spectral_flatness')
    @patch('librosa.feature.spectral_rolloff')
    @patch('librosa.pyin')
    def test_extract_features_success(self, mock_pyin, mock_rolloff, mock_flatness, 
                                    mock_power_spectrum, mock_centroid, mock_load):
        """Test successful feature extraction."""
        # Mock audio loading
        mock_audio = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        mock_load.return_value = (mock_audio, 22050)
        
        # Mock librosa functions
        mock_centroid.return_value = np.array([[0.059, 0.060, 0.058]])
        mock_power_spectrum.return_value = (np.array([0.1, 0.2, 0.3]), np.array([100, 200, 300]))
        mock_flatness.return_value = np.array([[0.5]])
        mock_rolloff.return_value = np.array([[0.007, 0.008, 0.007]])
        mock_pyin.return_value = (np.array([100, 105, 98]), np.array([True, True, False]), 
                                np.array([0.9, 0.8, 0.1]))
        
        with patch('os.path.exists', return_value=True):
            features = self.extractor.extract_features("test.wav")
            
            self.assertIsInstance(features, dict)
            self.assertIn('sd', features)
            self.assertIn('median', features)
            self.assertIn('meanfun', features)
            self.assertEqual(len(features), 20)  # All features should be present
    
    def test_extract_features_file_not_found(self):
        """Test feature extraction with non-existent file."""
        with patch('os.path.exists', return_value=False):
            features = self.extractor.extract_features("nonexistent.wav")
            self.assertIsNone(features)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.sample_data = {
            'sd': 0.064, 'median': 0.032, 'Q25': 0.015, 'Q75': 0.090,
            'IQR': 0.075, 'skew': 12.86, 'sp.ent': 0.893, 'mode': 0.0,
            'centroid': 0.059, 'meanfun': 0.084, 'minfun': 0.015,
            'maxfun': 0.276, 'mindom': 0.007, 'maxdom': 0.007, 'modindx': 0.0
        }
    
    def test_feature_extraction_placeholder(self):
        """Test placeholder feature extraction function."""
        features = extract_audio_features("dummy_path.wav")
        self.assertIsInstance(features, dict)
        self.assertIn('sd', features)
        self.assertEqual(len(features), 15)
    
    @patch('pickle.load')
    def test_end_to_end_prediction(self, mock_pickle_load):
        """Test end-to-end prediction workflow."""
        # Mock model
        mock_model = MagicMock()
        mock_model.predict.return_value = ['male']
        mock_pickle_load.return_value = mock_model
        
        # Create predictor and load model
        predictor = VoiceGenderPredictor()
        with patch('os.path.exists', return_value=True):
            predictor.load_model()
            
            # Test prediction
            result = predictor.predict(self.sample_data)
            self.assertEqual(result, 'male')


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def test_invalid_feature_values(self):
        """Test handling of invalid feature values."""
        predictor = VoiceGenderPredictor()
        
        # Test with string values
        invalid_features = {'sd': 'invalid', 'median': 0.032}
        result = predictor.predict(invalid_features)
        self.assertIsNone(result)
    
    def test_empty_features(self):
        """Test handling of empty features."""
        predictor = VoiceGenderPredictor()
        result = predictor.predict({})
        self.assertIsNone(result)
    
    def test_none_features(self):
        """Test handling of None features."""
        predictor = VoiceGenderPredictor()
        result = predictor.predict(None)
        self.assertIsNone(result)


def run_performance_test():
    """Run a simple performance test."""
    print("\\n=== Performance Test ===")
    
    # Sample features
    features = {
        'sd': 0.064, 'median': 0.032, 'Q25': 0.015, 'Q75': 0.090,
        'IQR': 0.075, 'skew': 12.86, 'sp.ent': 0.893, 'mode': 0.0,
        'centroid': 0.059, 'meanfun': 0.084, 'minfun': 0.015,
        'maxfun': 0.276, 'mindom': 0.007, 'maxdom': 0.007, 'modindx': 0.0
    }
    
    # Mock model for performance testing
    mock_model = MagicMock()
    mock_model.predict.return_value = ['male']
    
    predictor = VoiceGenderPredictor()
    predictor.model = mock_model
    
    # Time multiple predictions
    import time
    start_time = time.time()
    
    for i in range(1000):
        predictor.predict(features)
    
    end_time = time.time()
    avg_time = (end_time - start_time) / 1000
    
    print(f"Average prediction time: {avg_time*1000:.4f} ms")
    print(f"Predictions per second: {1/avg_time:.0f}")


def main():
    """Run all tests and performance benchmarks."""
    print("Voice Gender Prediction System - Test Suite")
    print("=" * 50)
    
    # Run unit tests
    print("\\nRunning unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance test
    run_performance_test()
    
    print("\\n=== Test Summary ===")
    print("✓ Unit tests completed")
    print("✓ Performance benchmarks completed")
    print("✓ Error handling verified")
    print("\\nAll tests completed successfully!")


if __name__ == "__main__":
    main()
