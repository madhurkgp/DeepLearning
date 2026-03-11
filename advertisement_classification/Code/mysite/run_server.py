#!/usr/bin/env python3
"""
Advertisement Classification System - Run Script
This script starts the Django development server for the advertisement classification web application.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import django
        import tensorflow
        import nltk
        print("✓ All major dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def download_nltk_data():
    """Download required NLTK data if not already present."""
    try:
        import nltk
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
        print("✓ NLTK data already downloaded")
    except LookupError:
        print("Downloading required NLTK data...")
        try:
            import nltk
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            print("✓ NLTK data downloaded successfully")
        except Exception as e:
            print(f"✗ Error downloading NLTK data: {e}")
            return False
    return True

def run_migrations():
    """Run Django migrations."""
    try:
        print("Running Django migrations...")
        subprocess.run([sys.executable, "manage.py", "makemigrations"], 
                      check=True, capture_output=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], 
                      check=True, capture_output=True)
        print("✓ Migrations completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Migration error: {e}")
        return False

def start_server():
    """Start the Django development server."""
    print("\n" + "="*50)
    print("ADVERTISEMENT CLASSIFICATION SYSTEM")
    print("="*50)
    print("\nStarting Django development server...")
    print("Server will be available at: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        # Start the server
        subprocess.run([sys.executable, "manage.py", "runserver"], check=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error starting server: {e}")
        return False
    return True

def main():
    """Main function to set up and run the application."""
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("Advertisement Classification System - Starting Up...")
    print("-" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Download NLTK data
    if not download_nltk_data():
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        sys.exit(1)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
