import os
import requests
import random

# Mood to Jamendo music parameters mapping
MOOD_TO_MUSIC_PARAMS = {
    'joy': {
        'tags': 'happy,upbeat,energetic,joyful,cheerful',
        'include_tags': 'happy',
        'mood': 'positive',
        'speed': 'fast'
    },
    'sadness': {
        'tags': 'sad,melancholic,emotional,sorrow,mellow',
        'include_tags': 'sad',
        'mood': 'negative',
        'speed': 'slow'
    },
    'anger': {
        'tags': 'angry,intense,aggressive,powerful,heavy',
        'include_tags': 'intense',
        'mood': 'negative',
        'speed': 'fast'
    },
    'fear': {
        'tags': 'dark,scary,tense,suspense,eerie',
        'include_tags': 'dark',
        'mood': 'negative',
        'speed': 'medium'
    },
    'surprise': {
        'tags': 'quirky,unusual,surprising,eccentric,different',
        'include_tags': 'quirky',
        'mood': 'positive',
        'speed': 'medium'
    },
    'neutral': {
        'tags': 'chill,ambient,relaxing,calm,instrumental',
        'include_tags': 'ambient',
        'mood': 'neutral',
        'speed': 'medium'
    }
}

class JamendoRecommender:
    def __init__(self):
        """Initialize the Jamendo recommender with API client ID"""
        self.client_id = os.environ.get('JAMENDO_CLIENT_ID')
        self.base_url = "https://api.jamendo.com/v3.0"
        
        if not self.client_id:
            self.connected = False
            print("Warning: Jamendo API client ID not found. Set JAMENDO_CLIENT_ID environment variable.")
        else:
            self.connected = True
            print("Jamendo API client ID found.")
    
    def is_connected(self):
        """Check if the Jamendo API client ID is set"""
        return self.connected
    
    def search_tracks(self, query, limit=5):
        """Search for tracks based on a query"""
        if not self.is_connected():
            return None
        
        try:
            params = {
                'client_id': self.client_id,
                'format': 'json',
                'namesearch': query,
                'limit': limit,
                'include': 'musicinfo'
            }
            
            response = requests.get(f"{self.base_url}/tracks/", params=params)
            if response.status_code != 200:
                print(f"Error searching tracks: {response.status_code}")
                return None
                
            results = response.json()
            tracks = []
            
            for item in results.get('results', []):
                track_name = item.get('name', 'Unknown Track')
                artist_name = item.get('artist_name', 'Unknown Artist')
                preview_url = item.get('audio', None)
                image_url = item.get('image', None)
                
                tracks.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'preview_url': preview_url,
                    'image_url': image_url
                })
            
            return tracks
        except Exception as e:
            print(f"Error searching tracks: {e}")
            return None
    
    def get_recommendations_by_mood(self, mood, limit=5):
        """Get personalized recommendations based on mood"""
        if not self.is_connected():
            return None
        
        try:
            # Get music parameters for the mood
            mood_params = MOOD_TO_MUSIC_PARAMS.get(mood, MOOD_TO_MUSIC_PARAMS['neutral'])
            
            # Create search parameters
            params = {
                'client_id': self.client_id,
                'format': 'json',
                'tags': mood_params['tags'],
                'limit': limit*2,  # Get more than needed to allow for filtering
                'include': 'musicinfo stats',
                'boost': 'popularity'
            }
            
            # Add specific mood parameter if it's supported
            if 'include_tags' in mood_params:
                params['include_tags'] = mood_params['include_tags']
            
            response = requests.get(f"{self.base_url}/tracks/", params=params)
            if response.status_code != 200:
                print(f"Error getting recommendations: {response.status_code}")
                return None
                
            results = response.json()
            tracks = []
            
            for item in results.get('results', []):
                # Only include tracks with audio previews
                if not item.get('audio'):
                    continue
                    
                track_name = item.get('name', 'Unknown Track')
                artist_name = item.get('artist_name', 'Unknown Artist')
                preview_url = item.get('audio', None)
                image_url = item.get('image', None)
                
                tracks.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'preview_url': preview_url,
                    'image_url': image_url
                })
            
            # Randomize selection and limit to requested number
            random.shuffle(tracks)
            return tracks[:limit]
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return None
    
    def get_trending_tracks(self, limit=5):
        """Get currently trending tracks"""
        if not self.is_connected():
            return None
        
        try:
            params = {
                'client_id': self.client_id,
                'format': 'json',
                'limit': limit,
                'include': 'musicinfo',
                'boost': 'popularity'
            }
            
            response = requests.get(f"{self.base_url}/tracks/", params=params)
            if response.status_code != 200:
                print(f"Error getting trending tracks: {response.status_code}")
                return None
                
            results = response.json()
            tracks = []
            
            for item in results.get('results', []):
                track_name = item.get('name', 'Unknown Track')
                artist_name = item.get('artist_name', 'Unknown Artist')
                preview_url = item.get('audio', None)
                image_url = item.get('image', None)
                
                tracks.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'preview_url': preview_url,
                    'image_url': image_url
                })
            
            return tracks
        except Exception as e:
            print(f"Error getting trending tracks: {e}")
            return None
    
    def get_tracks_by_genre(self, genre, limit=5):
        """Get tracks by genre"""
        if not self.is_connected():
            return None
        
        try:
            params = {
                'client_id': self.client_id,
                'format': 'json',
                'tags': genre,
                'limit': limit,
                'include': 'musicinfo'
            }
            
            response = requests.get(f"{self.base_url}/tracks/", params=params)
            if response.status_code != 200:
                print(f"Error getting tracks by genre: {response.status_code}")
                return None
                
            results = response.json()
            tracks = []
            
            for item in results.get('results', []):
                track_name = item.get('name', 'Unknown Track')
                artist_name = item.get('artist_name', 'Unknown Artist')
                preview_url = item.get('audio', None)
                image_url = item.get('image', None)
                
                tracks.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'preview_url': preview_url,
                    'image_url': image_url
                })
            
            return tracks
        except Exception as e:
            print(f"Error getting tracks by genre: {e}")
            return None
    
    def create_formatted_recommendations(self, mood, limit=5):
        """
        Get recommendations in the format compatible with the existing app
        Returns list of (track_name, artist_name, preview_url, image_url) tuples
        """
        recommendations = self.get_recommendations_by_mood(mood, limit)
        
        if not recommendations:
            return None
        
        formatted_recs = []
        for rec in recommendations:
            formatted_recs.append((
                rec['track_name'],
                rec['artist_name'],
                rec['preview_url'],
                rec['image_url']
            ))
        
        return formatted_recs

# Example usage
if __name__ == "__main__":
    recommender = JamendoRecommender()
    if recommender.is_connected():
        # Example: Get recommendations by mood
        happy_songs = recommender.get_recommendations_by_mood('joy', limit=3)
        print("\nHappy Songs:")
        for song in happy_songs:
            print(f"{song['track_name']} by {song['artist_name']}")
        
        # Example: Search for tracks
        search_results = recommender.search_tracks("piano", limit=2)
        print("\nSearch Results:")
        for song in search_results:
            print(f"{song['track_name']} by {song['artist_name']}")
    else:
        print("Not connected to Jamendo API. Set your client ID in environment variables.")
        print("export JAMENDO_CLIENT_ID='your_client_id'") 