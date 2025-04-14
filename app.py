import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from model import predict_mood, get_recommendations

# Set page configuration
st.set_page_config(
    page_title="Mood-Based Music Recommender",
    page_icon="🎵",
    layout="wide"
)

# App title and description
st.title("Mood-Based Music Recommender 🎵")
st.markdown("""
    This application analyzes your text input to detect your mood and recommends music that matches your emotional state.
    Enter your thoughts or feelings in the text box below, and we'll suggest songs that complement your mood!
""")

# Sidebar for app navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "How it works"])

if page == "Home":
    # Text input for mood analysis
    user_input = st.text_area("How are you feeling today? (Enter your thoughts or a paragraph about your day)", 
                             height=150,
                             placeholder="Today I'm feeling quite relaxed and content. The weather is nice and I'm looking forward to a peaceful evening...")
    
    # Analyze button
    if st.button("Analyze Mood & Get Recommendations"):
        if user_input:
            with st.spinner("Analyzing your mood..."):
                # Get mood prediction and confidence
                mood, confidence, mood_scores = predict_mood(user_input)
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Mood Analysis Results")
                    st.markdown(f"**Detected Mood:** {mood}")
                    st.markdown(f"**Confidence:** {confidence:.2f}%")
                    
                    # Create and display mood distribution chart
                    fig, ax = plt.subplots(figsize=(10, 6))
                    colors = sns.color_palette("viridis", len(mood_scores))
                    bars = ax.bar(mood_scores.keys(), mood_scores.values(), color=colors)
                    ax.set_title("Mood Distribution")
                    ax.set_ylabel("Score")
                    ax.set_ylim(0, 1.0)
                    
                    # Add value labels on top of bars
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                                f'{height:.2f}', ha='center', va='bottom', rotation=0)
                    
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("Music Recommendations")
                    with st.spinner("Finding songs that match your mood..."):
                        recommendations = get_recommendations(mood)
                        
                        if recommendations:
                            for i, (track, artist, preview_url, image_url) in enumerate(recommendations, 1):
                                st.markdown(f"### {i}. {track} - {artist}")
                                
                                # Create two columns for image and audio preview
                                img_col, audio_col = st.columns([1, 3])
                                
                                with img_col:
                                    if image_url:
                                        st.image(image_url, width=100)
                                
                                with audio_col:
                                    if preview_url:
                                        st.audio(preview_url, format="audio/mp3")
                                    else:
                                        st.write("No preview available")
                        else:
                            st.warning("Could not retrieve recommendations.")
        else:
            st.error("Please enter some text about how you're feeling!")

elif page == "About":
    st.header("About this Project")
    st.write("""
    This mood-based music recommender uses natural language processing (NLP) and sentiment analysis 
    to understand your emotional state and recommend music that matches or complements your mood.
    
    The system uses:
    - **Keyword-based sentiment analysis** to analyze text sentiment
    - **Custom mood classification** to map text to emotional states
    - **Curated music recommendations** for different moods
    
    Created as a demonstration of how machine learning can be used to enhance personalized recommendations.
    """)
    
    st.subheader("Technologies Used")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("- Python")
        st.markdown("- Streamlit")
        st.markdown("- Regular Expressions")
    
    with col2:
        st.markdown("- Pandas")
        st.markdown("- NumPy")
        st.markdown("- Keyword-based Analysis")
    
    with col3:
        st.markdown("- Matplotlib")
        st.markdown("- Seaborn")
        st.markdown("- Custom Scoring Algorithm")

elif page == "How it works":
    st.header("How it Works")
    
    st.subheader("1. Text Analysis")
    st.write("""
    When you enter text, our system uses keyword pattern matching to determine the emotional tone
    of your text and classify it into categories such as 'happy', 'sad', 'angry', etc.
    """)
    
    st.subheader("2. Mood Mapping")
    st.write("""
    After identifying the keywords that suggest different emotions, we calculate the dominant mood 
    and confidence score based on the frequency and distribution of these mood indicators.
    """)
    
    st.subheader("3. Music Recommendation")
    st.write("""
    The app has a curated database of songs for each mood category. Once your dominant mood is detected,
    it suggests music that complements that emotional state.
    """)
    
    st.subheader("4. Mood-Music Relationship")
    st.image("https://miro.medium.com/max/1400/1*_Fin1f_Kt7J-VEyzk4Q7vg.png", 
            caption="Example of a Valence-Arousal emotion model and how it relates to music")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and Python") 