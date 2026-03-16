#!/usr/bin/env python3
"""
Audio Feature Extraction Module

This module provides functionality to extract voice features from audio files
using librosa for audio processing.
"""

import librosa
import numpy as np
import pandas as pd
import logging
from typing import Optional, Dict, Any
from scipy import stats
from scipy.stats import skew, kurtosis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioFeatureExtractor:
    """
    A class for extracting voice features from audio files.
    """
    
    def __init__(self, sample_rate: int = 22050):
        """
        Initialize the feature extractor.
        
        Args:
            sample_rate: Audio sample rate for processing.
        """
        self.sample_rate = sample_rate
    
    def load_audio(self, audio_path: str) -> Optional[np.ndarray]:
        """
        Load audio file and return the waveform.
        
        Args:
            audio_path: Path to the audio file.
            
        Returns:
            Audio waveform as numpy array, or None if loading fails.
        """
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            if len(y) == 0:
                raise ValueError("Audio file is empty")
            
            logger.info(f"Audio loaded successfully: {audio_path}")
            return y
            
        except Exception as e:
            logger.error(f"Error loading audio file {audio_path}: {str(e)}")
            return None
    
    def extract_features(self, audio_path: str) -> Optional[Dict[str, float]]:
        """
        Extract voice features from an audio file.
        
        Args:
            audio_path: Path to the audio file.
            
        Returns:
            Dictionary of extracted features, or None if extraction fails.
        """
        try:
            # Load audio
            y = self.load_audio(audio_path)
            if y is None:
                return None
            
            # Extract features
            features = {}
            
            # Basic frequency domain features
            features['meanfreq'] = np.mean(librosa.feature.spectral_centroid(y=y, sr=self.sample_rate))
            features['sd'] = np.std(librosa.feature.spectral_centroid(y=y, sr=self.sample_rate))
            
            # Compute spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=self.sample_rate)[0]
            features['median'] = np.median(spectral_centroids)
            features['Q25'] = np.percentile(spectral_centroids, 25)
            features['Q75'] = np.percentile(spectral_centroids, 75)
            features['IQR'] = features['Q75'] - features['Q25']
            features['skew'] = skew(spectral_centroids)
            features['kurt'] = kurtosis(spectral_centroids)
            
            # Spectral entropy
            power_spectrum, freqs = librosa.power_spectrum(y, sr=self.sample_rate)
            power_spectrum = power_spectrum / np.sum(power_spectrum)  # Normalize
            features['sp.ent'] = -np.sum(power_spectrum * np.log2(power_spectrum + 1e-10))
            
            # Spectral flatness
            features['sfm'] = np.mean(librosa.feature.spectral_flatness(y=y))
            
            # Mode frequency
            features['mode'] = stats.mode(spectral_centroids, keepdims=True)[0][0]
            
            # Frequency centroid (already computed as meanfreq)
            features['centroid'] = features['meanfreq']
            
            # Fundamental frequency features
            f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
            
            # Filter out unvoiced frames
            voiced_f0 = f0[voiced_flag]
            
            if len(voiced_f0) > 0:
                features['meanfun'] = np.mean(voiced_f0)
                features['minfun'] = np.min(voiced_f0)
                features['maxfun'] = np.max(voiced_f0)
            else:
                # Default values if no voiced frames detected
                features['meanfun'] = 0.0
                features['minfun'] = 0.0
                features['maxfun'] = 0.0
            
            # Dominant frequency features
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=self.sample_rate)
            features['meandom'] = np.mean(spectral_rolloff)
            features['mindom'] = np.min(spectral_rolloff)
            features['maxdom'] = np.max(spectral_rolloff)
            features['dfrange'] = features['maxdom'] - features['mindom']
            
            # Modulation index
            features['modindx'] = features['dfrange'] / (features['maxdom'] + 1e-10)
            
            logger.info(f"Features extracted successfully for {audio_path}")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features from {audio_path}: {str(e)}")
            return None
    
    def extract_features_batch(self, audio_paths: list) -> pd.DataFrame:
        """
        Extract features from multiple audio files.
        
        Args:
            audio_paths: List of audio file paths.
            
        Returns:
            DataFrame with extracted features.
        """
        features_list = []
        
        for audio_path in audio_paths:
            features = self.extract_features(audio_path)
            if features:
                features['audio_path'] = audio_path
                features_list.append(features)
            else:
                logger.warning(f"Failed to extract features from {audio_path}")
        
        if features_list:
            return pd.DataFrame(features_list)
        else:
            return pd.DataFrame()


def extract_features_from_audio(audio_path: str, sample_rate: int = 22050) -> Optional[Dict[str, float]]:
    """
    Convenience function to extract features from a single audio file.
    
    Args:
        audio_path: Path to the audio file.
        sample_rate: Audio sample rate.
        
    Returns:
        Dictionary of extracted features.
    """
    extractor = AudioFeatureExtractor(sample_rate)
    return extractor.extract_features(audio_path)


if __name__ == "__main__":
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description='Extract voice features from audio files')
    parser.add_argument('audio_path', help='Path to audio file')
    parser.add_argument('--output', help='Output CSV file for features')
    parser.add_argument('--sample-rate', type=int, default=22050, help='Sample rate')
    
    args = parser.parse_args()
    
    # Extract features
    features = extract_features_from_audio(args.audio_path, args.sample_rate)
    
    if features:
        print("Extracted features:")
        for feature, value in features.items():
            print(f"{feature}: {value:.6f}")
        
        # Save to CSV if requested
        if args.output:
            df = pd.DataFrame([features])
            df.to_csv(args.output, index=False)
            print(f"Features saved to {args.output}")
    else:
        print("Feature extraction failed")
