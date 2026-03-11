# WhatsApp Chat Analyzer

A Flask-based web application to analyze WhatsApp chat exports and generate insights.

## Features

- 📊 Message statistics (total messages, words, media, links)
- 🏆 Most active users analysis
- ☁️ Word cloud generation
- 📝 Most common words analysis
- 😊 Emoji usage statistics
- 📅 Monthly timeline analysis
- 📆 Activity maps (daily and monthly patterns)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Upload your WhatsApp chat export file (.txt format)

4. Select a user or "Overall" for group analysis

5. View the comprehensive analysis results

## WhatsApp Chat Export

To get your WhatsApp chat data:
1. Open WhatsApp
2. Go to the chat you want to analyze
3. Tap on the three dots (More options)
4. Select "Export chat"
5. Choose "Without media" for smaller file size
6. Save the .txt file

## File Structure

```
whatsap_chat_analyzer/
├── app.py              # Main Flask application
├── preprocess.py       # Data preprocessing functions
├── stats.py           # Statistical analysis functions
├── requirements.txt    # Python dependencies
├── stop_hinglish.txt  # Stop words for text processing
├── templates/         # HTML templates
│   ├── index.html     # File upload page
│   ├── analysis.html  # User selection page
│   └── results.html   # Analysis results page
└── README.md          # This file
```

## Dependencies

- Flask: Web framework
- Pandas: Data manipulation
- Matplotlib: Data visualization
- WordCloud: Word cloud generation
- Emoji: Emoji analysis
- URLExtract: Link extraction
- NumPy: Numerical operations

## Notes

- The application temporarily stores processed data as `temp_data.csv`
- All visualizations are generated dynamically and embedded as base64 images
- The app supports both individual user analysis and overall group analysis
