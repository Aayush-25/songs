import os
import re
import numpy as np
import pandas as pd
import random

# Import Jamendo integration if available
try:
    from jamendo_integration import JamendoRecommender
    jamendo_available = True
except ImportError:
    jamendo_available = False

# Initialize Jamendo recommender if available
jamendo_recommender = None
if jamendo_available:
    jamendo_recommender = JamendoRecommender()

# Simple sentiment analysis using keyword matching
def simple_sentiment_analysis(text):
    """
    Very basic sentiment analysis using keyword matching.
    Returns a mood and confidence score.
    """
    # Convert to lowercase for case-insensitive matching
    text = text.lower()
    
    # Define mood keywords
    mood_keywords = {
        'joy': ['happy', 'joy', 'exciting', 'excited', 'great', 'glad', 'wonderful', 'amazing', 'love', 'smile', 'laugh', 'cheerful', 'delighted', 'overjoyed', 'thrilled'],
        'sadness': ['sad', 'upset', 'unhappy', 'depressed', 'miserable', 'heartbroken', 'grief', 'blue', 'sorrow', 'crying', 'tears', 'lonely', 'disappointed', 'hurt', 'heartache'],
        'anger': ['angry', 'mad', 'furious', 'outraged', 'annoyed', 'frustrating', 'frustrated', 'irritated', 'rage', 'hate', 'resentment', 'hostile', 'bitter', 'infuriated', 'enraged'],
        'fear': ['afraid', 'scared', 'frightened', 'terrified', 'anxious', 'nervous', 'worried', 'panic', 'horror', 'terror', 'dread', 'concern', 'alarmed', 'distressed', 'uneasy'],
        'surprise': ['surprised', 'shock', 'astonished', 'amazed', 'unexpected', 'wow', 'stunned', 'startled', 'speechless', 'disbelief', 'bewildered', 'astounded', 'dumbfounded', 'unexpected', 'awe'],
        'neutral': ['okay', 'fine', 'alright', 'normal', 'calm', 'steady', 'balanced', 'average', 'so-so', 'content', 'adequate', 'satisfactory', 'passable', 'tolerable', 'moderate']
    }
    
    # Count occurrences of each mood's keywords
    mood_scores = {}
    for mood, keywords in mood_keywords.items():
        count = sum(1 for keyword in keywords if re.search(r'\b' + keyword + r'\b', text))
        mood_scores[mood] = count
    
    # Find dominant mood (max count)
    total_matches = sum(mood_scores.values())
    
    # If no matches found, default to neutral
    if total_matches == 0:
        return 'neutral', 50, {'joy': 0.1, 'sadness': 0.1, 'anger': 0.1, 'fear': 0.1, 'surprise': 0.1, 'neutral': 0.5}
    
    # Find the mood with the highest count
    dominant_mood = max(mood_scores, key=mood_scores.get)
    
    # Normalize scores to get confidence (0-100)
    normalized_scores = {mood: (count / total_matches) for mood, count in mood_scores.items()}
    confidence = normalized_scores[dominant_mood] * 100
    
    # If confidence is too low, default to neutral
    if confidence < 30:
        dominant_mood = 'neutral'
        confidence = 50
    
    # Create visualization-friendly scores
    vis_scores = {mood: 0.1 for mood in mood_keywords.keys()}
    for mood, score in normalized_scores.items():
        if score > 0:
            vis_scores[mood] = score
    
    return dominant_mood, confidence, vis_scores

# Function to use instead of predict_mood from transformer model
def predict_mood(text):
    """
    Predict the mood of the given text using simple keyword-based approach.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        tuple: (dominant_emotion, confidence, emotion_scores)
    """
    return simple_sentiment_analysis(text)

# Static database of music recommendations
MUSIC_RECOMMENDATIONS = {
    'joy': [
        ("Happy", "Pharrell Williams", "https://open.spotify.com/embed/track/60nZcImufyMA1MKQY3dcCO", "https://i.scdn.co/image/ab67616d0000b273e56f7b6ad45b695ad7b8ebe7"),
        ("Walking on Sunshine", "Katrina & The Waves", None, "https://i.scdn.co/image/ab67616d0000b273441d29deec3c38d7f8541856"),
        ("Uptown Funk", "Mark Ronson ft. Bruno Mars", None, "https://i.scdn.co/image/ab67616d0000b273e94e3bfa3af2fa67bda8c5f0"),
        ("Can't Stop the Feeling!", "Justin Timberlake", None, "https://i.scdn.co/image/ab67616d0000b2735f4e9d2c670e4b2b896e2aa2"),
        ("Good as Hell", "Lizzo", None, "https://i.scdn.co/image/ab67616d0000b273e4e28efdf2f54386b9d3c3a0"),
        ("Don't Stop Me Now", "Queen", None, "https://i.scdn.co/image/ab67616d0000b273056e90910cbaf5c5b892aeba"),
        ("I Gotta Feeling", "Black Eyed Peas", None, "https://i.scdn.co/image/ab67616d0000b2736b5e2f96d66d084dafa3f0a9"),
        ("Shake It Off", "Taylor Swift", None, "https://i.scdn.co/image/ab67616d0000b27302e1bfa4bdf40cd7c4cd97b5"),
        ("Dancing Queen", "ABBA", None, "https://i.scdn.co/image/ab67616d0000b2733427f4099d0e3a21d25747f5"),
        ("Dynamite", "BTS", None, "https://i.scdn.co/image/ab67616d0000b273a6a151ed587bda32496a9a16"),
        ("Celebration", "Kool & The Gang", None, "https://i.scdn.co/image/ab67616d0000b2735a1d909af70d94f79c5b86dc"),
        ("Best Day of My Life", "American Authors", None, "https://i.scdn.co/image/ab67616d0000b27363f83e32be6b169a693acda1")
    ],
    'sadness': [
        ("Someone Like You", "Adele", None, "https://i.scdn.co/image/ab67616d0000b2732118bf9b198b05a95ded6300"),
        ("Fix You", "Coldplay", None, "https://i.scdn.co/image/ab67616d0000b273fa9247b03d9bc877c72b352c"),
        ("All I Want", "Kodaline", None, "https://i.scdn.co/image/ab67616d0000b273f0fd9dad63242d8830cca2d5"),
        ("Hurt", "Johnny Cash", None, "https://i.scdn.co/image/ab67616d0000b2736f4f62da3d811b6501a69d29"),
        ("Nothing Compares 2 U", "Sinéad O'Connor", None, "https://i.scdn.co/image/ab67616d0000b2736aa1dfa0a98baa542251df6a"),
        ("Hello", "Adele", None, "https://i.scdn.co/image/ab67616d0000b2732118bf9b198b05a95ded6300"),
        ("Skinny Love", "Bon Iver", None, "https://i.scdn.co/image/ab67616d0000b273daa31ce0bf7d9e40c3c64cd6"),
        ("The Night We Met", "Lord Huron", None, "https://i.scdn.co/image/ab67616d0000b273cad190f1a73c024e5a15c0e0"),
        ("Everybody Hurts", "R.E.M.", None, "https://i.scdn.co/image/ab67616d0000b2737d5dc0a6ae64cd463af88ebd"),
        ("Mad World", "Gary Jules", None, "https://i.scdn.co/image/ab67616d0000b273d43c57624966834de96ec8f7"),
        ("Say Something", "A Great Big World & Christina Aguilera", None, "https://i.scdn.co/image/ab67616d0000b2735729bc448a8c8039a850cab5"),
        ("Hallelujah", "Jeff Buckley", None, "https://i.scdn.co/image/ab67616d0000b2738b38c22503f8adcc0fb8abfa")
    ],
    'anger': [
        ("Break Stuff", "Limp Bizkit", None, "https://i.scdn.co/image/ab67616d0000b273e07b79e965a82facf407b8db"),
        ("Killing In The Name", "Rage Against The Machine", None, "https://i.scdn.co/image/ab67616d0000b273c9e084dcb7527827e532a13d"),
        ("Master of Puppets", "Metallica", None, "https://i.scdn.co/image/ab67616d0000b273668e3aea90205887a5cf9a8a"),
        ("Bodies", "Drowning Pool", None, "https://i.scdn.co/image/ab67616d0000b273d5f3cea8d3d05337963c22e3"),
        ("Bulls on Parade", "Rage Against The Machine", None, "https://i.scdn.co/image/ab67616d0000b273c9e084dcb7527827e532a13d"),
        ("Last Resort", "Papa Roach", None, "https://i.scdn.co/image/ab67616d0000b273fe1a9a451d89a872810d7c6a"),
        ("This Fire Burns", "Killswitch Engage", None, "https://i.scdn.co/image/ab67616d0000b2734a95efb1499e4f7efc8ea5e7"),
        ("Chop Suey!", "System Of A Down", None, "https://i.scdn.co/image/ab67616d0000b273c65f8d04502eedcd684bb615"),
        ("Down with the Sickness", "Disturbed", None, "https://i.scdn.co/image/ab67616d0000b273b4ad7ebaf4575f120eb3f193"),
        ("Du Hast", "Rammstein", None, "https://i.scdn.co/image/ab67616d0000b27344234cd5f20a0e24fde9c59a"),
        ("Numb", "Linkin Park", None, "https://i.scdn.co/image/ab67616d0000b27344234cd5f20a0e24fde9c59a"),
        ("Had Enough", "Breaking Benjamin", None, "https://i.scdn.co/image/ab67616d0000b2733c0b81c91497733400702673")
    ],
    'fear': [
        ("Thriller", "Michael Jackson", None, "https://i.scdn.co/image/ab67616d0000b273c29e8c3f3d41c8b6bac2747c"),
        ("Disturbia", "Rihanna", None, "https://i.scdn.co/image/ab67616d0000b27325dddab458f140cb0bfcf0fe"),
        ("Sweet Dreams", "Marilyn Manson", None, "https://i.scdn.co/image/ab67616d0000b2731e79c75b5480f9dbbcf1f19e"),
        ("Fear of the Dark", "Iron Maiden", None, "https://i.scdn.co/image/ab67616d0000b273c35a7a6e6126a8f4e1e0b09e"),
        ("Pet Sematary", "Ramones", None, "https://i.scdn.co/image/ab67616d0000b273e9abab84f31e7e3119adb00c"),
        ("Enter Sandman", "Metallica", None, "https://i.scdn.co/image/ab67616d0000b27368172a3da1b5efe02da4bb7f"),
        ("The Number of the Beast", "Iron Maiden", None, "https://i.scdn.co/image/ab67616d0000b273e5b5ab3bcae3c039be9f6fbd"),
        ("Fear", "Kendrick Lamar", None, "https://i.scdn.co/image/ab67616d0000b27312a76d1b13ef07187fbf30e2"),
        ("Psycho", "Muse", None, "https://i.scdn.co/image/ab67616d0000b273ea7caaff71dea1051d49b2fe"),
        ("Bring Me To Life", "Evanescence", None, "https://i.scdn.co/image/ab67616d0000b2732289f282f249a7f5387333bd"),
        ("Nightmare", "Avenged Sevenfold", None, "https://i.scdn.co/image/ab67616d0000b273587d1b4f4fc261247fa01a26"),
        ("Monster", "Skillet", None, "https://i.scdn.co/image/ab67616d0000b2732289f282f249a7f5387333bd")
    ],
    'surprise': [
        ("What Does the Fox Say?", "Ylvis", None, "https://i.scdn.co/image/ab67616d0000b2733a4e8778e91d57f7d54bfe29"),
        ("Never Gonna Give You Up", "Rick Astley", None, "https://i.scdn.co/image/ab67616d0000b273d87bbd739cca0e5fb27ec8a9"),
        ("Call Me Maybe", "Carly Rae Jepsen", None, "https://i.scdn.co/image/ab67616d0000b273fa7a2db96e42f2a5b61058d4"),
        ("Gangnam Style", "PSY", None, "https://i.scdn.co/image/ab67616d0000b273a7dd2abab0d0aabfde72c508"),
        ("Take On Me", "a-ha", None, "https://i.scdn.co/image/ab67616d0000b273b7ea3bfa3c1daf3d29b19c7e"),
        ("This Is Halloween", "The Citizens of Halloween", None, "https://i.scdn.co/image/ab67616d0000b27388d07f4e6a22b2b6114a9f17"),
        ("I'm Gonna Be (500 Miles)", "The Proclaimers", None, "https://i.scdn.co/image/ab67616d0000b2731fb3ae26e1813162eb6a0d63"),
        ("Funky Town", "Lipps Inc", None, "https://i.scdn.co/image/ab67616d0000b273eef37db6cdecf50ece7fe8c5"),
        ("The Safety Dance", "Men Without Hats", None, "https://i.scdn.co/image/ab67616d0000b2736cc02cb1fe72dd56cd47c4da"),
        ("Barbie Girl", "Aqua", None, "https://i.scdn.co/image/ab67616d0000b273dc4c2c5cdabe36b8c4ef8ca8"),
        ("Cotton Eye Joe", "Rednex", None, "https://i.scdn.co/image/ab67616d0000b2737c7359b16409d36c2bb796ec"),
        ("Macarena", "Los Del Rio", None, "https://i.scdn.co/image/ab67616d0000b273eb3a4564d3ebe0ef7b5a9794")
    ],
    'neutral': [
        ("Somewhere Only We Know", "Keane", None, "https://i.scdn.co/image/ab67616d0000b273649b7aff31f3c4e08c71498b"),
        ("Castle on the Hill", "Ed Sheeran", None, "https://i.scdn.co/image/ab67616d0000b273ba5db46f4b838ef6027e6f96"),
        ("Here Comes the Sun", "The Beatles", None, "https://i.scdn.co/image/ab67616d0000b273dc30583ba717007b00cceb25"),
        ("The Middle", "Jimmy Eat World", None, "https://i.scdn.co/image/ab67616d0000b273fe2f610e6e07e38e4b6bcf9c"),
        ("Fast Car", "Tracy Chapman", None, "https://i.scdn.co/image/ab67616d0000b2732fbd9fb3f02f11bc0d79467c"),
        ("Dreams", "Fleetwood Mac", None, "https://i.scdn.co/image/ab67616d0000b273e52a59a28efa4773dd2bfe1b"),
        ("Africa", "Toto", None, "https://i.scdn.co/image/ab67616d0000b2739dacfaad9df5479a9a90f244"),
        ("Landslide", "Fleetwood Mac", None, "https://i.scdn.co/image/ab67616d0000b273e52a59a28efa4773dd2bfe1b"),
        ("Imagine", "John Lennon", None, "https://i.scdn.co/image/ab67616d0000b273d8d9acdf4f25f0237992756c"),
        ("Tiny Dancer", "Elton John", None, "https://i.scdn.co/image/ab67616d0000b2735854313e8e3a5c67b923e6c7"),
        ("Stand By Me", "Ben E. King", None, "https://i.scdn.co/image/ab67616d0000b273551a69751740f220f4e865d1"),
        ("Hotel California", "Eagles", None, "https://i.scdn.co/image/ab67616d0000b273e1e3f8511cd8509c7d6e8e7d")
    ]
}

def get_recommendations(mood, limit=5):
    """
    Get music recommendations based on the detected mood.
    
    Args:
        mood (str): The detected mood
        limit (int): Number of recommendations to return
        
    Returns:
        list: List of (track_name, artist_name, preview_url, image_url) tuples
    """
    # First try to get recommendations from Jamendo if available
    if jamendo_available and jamendo_recommender and jamendo_recommender.is_connected():
        try:
            jamendo_recs = jamendo_recommender.create_formatted_recommendations(mood, limit)
            if jamendo_recs:
                print(f"Using Jamendo recommendations for mood: {mood}")
                return jamendo_recs
        except Exception as e:
            print(f"Error getting Jamendo recommendations: {e}")
    
    # Fall back to static recommendations if Jamendo is not available
    print(f"Using static recommendations for mood: {mood}")
    mood_recommendations = MUSIC_RECOMMENDATIONS.get(mood, MUSIC_RECOMMENDATIONS['neutral'])
    
    # If we want randomized recommendations, uncomment the next line
    random.shuffle(mood_recommendations)
    
    # Limit the number of recommendations
    return mood_recommendations[:limit] 