# Course Recommendation System

A Flask-based web application that provides course recommendations using content-based filtering and cosine similarity on Udemy course data.

## Features

- **Course Recommendations**: Get personalized course recommendations based on course titles
- **Search Functionality**: Search for courses by partial title matches
- **Interactive Dashboard**: Visual analytics showing course statistics, trends, and insights
- **Responsive UI**: Modern Bootstrap-based interface with course cards and navigation

## Project Structure

```
Course_Recomendation_System/
├── app.py                 # Main Flask application
├── dashboard.py           # Dashboard data processing functions
├── templates/
│   ├── index.html        # Main recommendation interface
│   └── dashboard.html    # Analytics dashboard
├── UdemyCleanedTitle.csv # Course dataset
├── EDA on UdemyDataset.ipynb # Exploratory data analysis
├── Course Recommendation System.ipynb # Recommendation logic
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Required Packages
```bash
pip install flask pandas numpy scikit-learn neattext matplotlib seaborn
```

### Setup
1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure the `UdemyCleanedTitle.csv` file is in the project root

## Usage

### Running the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Features

#### Home Page (`/`)
- Enter a course name to get recommendations
- Use popular course suggestion buttons for quick access
- View recommended courses with links to Udemy

#### Dashboard (`/dashboard`)
- Course distribution by subject and level
- Subscriber analytics and trends
- Profit analysis by year and month
- Interactive charts and visualizations

## How It Works

### Recommendation Algorithm
1. **Text Preprocessing**: Course titles are cleaned by removing stopwords and special characters
2. **Feature Extraction**: Uses CountVectorizer to convert titles to numerical features
3. **Similarity Calculation**: Computes cosine similarity between course vectors
4. **Recommendation**: Returns top N most similar courses based on similarity scores

### Search Functionality
- Performs case-insensitive partial string matching
- Results sorted by subscriber count
- Returns top 6 matching courses

## API Endpoints

### `GET /`
- Renders the main recommendation interface
- Accepts POST requests with course name for recommendations

### `POST /`
- **Parameters**: `course` (course name)
- **Returns**: Recommended courses or search results

### `GET /dashboard`
- Renders the analytics dashboard
- Displays various charts and statistics

## Dataset

The system uses the `UdemyCleanedTitle.csv` file containing:
- Course titles
- Subject categories
- Difficulty levels
- Pricing information
- Subscriber counts
- Review counts
- Publication timestamps

## Known Issues & Limitations

### Current Issues
- Hardcoded index removal in data processing (line 39 in dashboard.py)
- Bare exception handling in main application
- Debug mode enabled (security risk in production)
- No input validation for user searches

### Limitations
- Recommendations based solely on course titles
- No user preference learning
- Limited to courses in the dataset
- Performance issues with large datasets

## Future Improvements

### Planned Features
- [ ] User authentication and profiles
- [ ] Collaborative filtering recommendations
- [ ] Course rating integration
- [ ] Advanced search filters
- [ ] Mobile app version

### Technical Improvements
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Redis caching for similarity matrix
- [ ] API rate limiting
- [ ] Comprehensive error handling
- [ ] Unit tests and integration tests
- [ ] Docker containerization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with Udemy's terms of service when using course data.

## Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 4, JavaScript
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Visualization**: Chart.js, Matplotlib, Seaborn
- **Text Processing**: Neattext

## Performance Considerations

- Cosine similarity matrix is recalculated on each request (consider caching)
- CSV file loaded on every request (consider database storage)
- Large datasets may cause memory issues

## Security Notes

- Debug mode should be disabled in production
- Input validation should be implemented
- HTTPS should be used in production
- Consider implementing CSRF protection

## Support

For issues and questions:
1. Check the Known Issues section
2. Review the code comments
3. Create an issue with detailed description

---

**Note**: This is a learning project demonstrating content-based recommendation systems. For production use, additional security, scalability, and performance optimizations are required.
