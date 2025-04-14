# Mood-Based Music Recommender 🎵

This application analyzes your text input to detect your mood and recommends music that matches your emotional state.

## Features

- **Text Sentiment Analysis**: Analyzes text to detect emotional states
- **Mood Detection**: Identifies emotional states from text input
- **Music Recommendations**: Suggests songs that match detected moods
- **Visualization**: Displays mood distribution with interactive charts
- **Jamendo Integration**: (Optional) Connect to Jamendo API for independent artist music recommendations

## Demo

![App Demo](https://i.imgur.com/placeholder.gif)

## Setup Instructions

### Prerequisites

- Python 3.8+ installed
- Jamendo Developer account (optional, for real-time recommendations)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/mood-music-recommender.git
   cd mood-music-recommender
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. (Optional) Set up Jamendo API credentials for enhanced recommendations:
   - Create a Jamendo Developer account at [developer.jamendo.com](https://developer.jamendo.com/)
   - Create a new application in the Jamendo Developer Dashboard
   - Copy your Client ID
   - Create a .env file in the root directory:
     ```
     JAMENDO_CLIENT_ID="your_client_id"
     ```
   - Load environment variables:
     ```
     source .env  # On Linux/Mac
     ```

   Note: If Jamendo credentials are not provided, the app will use a curated list of song recommendations.

### Running the Application

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

## How It Works

1. **Text Analysis**: Enter your thoughts or feelings in the text box
2. **Mood Detection**: The app analyzes your text to identify emotional keywords
3. **Music Mapping**: Detected emotions are mapped to music moods
4. **Recommendation**: The app suggests songs that match your emotional state

### Two Recommendation Modes

#### 1. Static Recommendations (Default)
- Uses a pre-defined database of songs for each mood
- Works without any external API connections
- Provides consistent recommendations based on the detected mood

#### 2. Jamendo API Recommendations (Enhanced)
- Connects to Jamendo's API to generate real-time recommendations
- Creates personalized suggestions based on mood tags and genres
- Requires Jamendo Developer credentials
- Provides a wider variety of up-to-date recommendations from independent artists
- All music is license-friendly and can be used freely

## Technology Stack

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **Regular Expressions**: For keyword-based sentiment analysis
- **Jamendo API**: (Optional) Enhanced music recommendations from independent artists
- **Matplotlib/Seaborn**: Data visualization
- **Pandas/NumPy**: Data handling
- **Requests**: HTTP library for API interaction

## Future Enhancements

- Enhanced sentiment analysis with machine learning models
- User feedback integration to improve recommendations
- Playlist creation and export to music services
- Multi-language support
- Mobile application version

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Streamlit ❤️
- Optional integration with Jamendo API for independent artist music
- Jamendo provides music from independent artists with Creative Commons and other open licenses 