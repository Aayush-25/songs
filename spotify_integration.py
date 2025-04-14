import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Mood to Spotify music features mapping
MOOD_TO_MUSIC_FEATURES = {
    'joy': {
        'valence': (0.7, 1.0),
        'energy': (0.6, 1.0),
        'tempo': (90, 150),
        'mode': 1,  # Major key
        'seed_genres': ['happy', 'pop', 'dance', 'disco', 'funk']
    },
    'sadness': {
        'valence': (0.0, 0.4),
        'energy': (0.0, 0.5),
        'tempo': (60, 100),
        'mode': 0,  # Minor key
        'seed_genres': ['sad', 'blues', 'piano', 'indie', 'folk']
    },
    'anger': {
        'valence': (0.1, 0.4),
        'energy': (0.7, 1.0),
        'tempo': (120, 180),
        'mode': 0,  # Minor key
        'seed_genres': ['rock', 'metal', 'hardcore', 'dubstep', 'grunge']
    },
    'fear': {
        'valence': (0.0, 0.3),
        'energy': (0.3, 0.6),
        'tempo': (70, 120),
        'mode': 0,  # Minor key
        'seed_genres': ['ambient', 'soundtrack', 'experimental', 'classical', 'instrumental']
    },
    'surprise': {
        'valence': (0.5, 0.8),
        'energy': (0.6, 0.9),
        'tempo': (100, 140),
        'mode': None,  # Any key
        'seed_genres': ['electronic', 'pop', 'dance', 'edm', 'techno']
    },
    'neutral': {
        'valence': (0.3, 0.7),
        'energy': (0.3, 0.7),
        'tempo': (80, 120),
        'mode': None,  # Any key
        'seed_genres': ['indie', 'folk', 'chill', 'acoustic', 'alternative']
    }
}

class SpotifyRecommender:
    def __init__(self):
        """Initialize the Spotify recommender with API credentials"""
        client_id = os.environ.get('SPOTIFY_CLIENT_ID')
        client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            self.sp = None
            print("Warning: Spotify API credentials not found. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")
        else:
            try:
                client_credentials_manager = SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                )
                self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                print("Successfully connected to Spotify API")
            except Exception as e:
                self.sp = None
                print(f"Error connecting to Spotify API: {e}")
    
    def is_connected(self):
        """Check if the Spotify client is initialized"""
        return self.sp is not None
    
    def search_tracks(self, query, limit=5):
        """Search for tracks based on a query"""
        if not self.is_connected():
            return None
        
        try:
            results = self.sp.search(q=query, type='track', limit=limit)
            tracks = []
            
            for item in results['tracks']['items']:
                track_name = item['name']
                artist_name = item['artists'][0]['name']
                preview_url = item['preview_url']
                image_url = item['album']['images'][0]['url'] if item['album']['images'] else None
                spotify_url = item['external_urls']['spotify']
                
                tracks.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'preview_url': preview_url,
                    'image_url': image_url,
                    'spotify_url': spotify_url
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
            # Get music features for the mood
            features = MOOD_TO_MUSIC_FEATURES.get(mood, MOOD_TO_MUSIC_FEATURES['neutral'])
            seed_genres = features['seed_genres']
            valence_range = features['valence']
            energy_range = features['energy']
            tempo_range = features['tempo']
            
            # Randomly select seed genres (max 5)
            selected_genres = random.sample(seed_genres, min(len(seed_genres), 3))
            
            # Get recommendations
            results = self.sp.recommendations(
                seed_genres=selected_genres,
                target_valence=(valence_range[0] + valence_range[1]) / 2,
                min_valence=valence_range[0],
                max_valence=valence_range[1],
                target_energy=(energy_range[0] + energy_range[1]) / 2,
                min_energy=energy_range[0],
                max_energy=energy_range[1],
                target_tempo=(tempo_range[0] + tempo_range[1]) / 2,
                min_tempo=tempo_range[0],
                max_tempo=tempo_range[1],
                limit=limit
            )
            
            # Format recommendations
            recommendations = []
            for track in results['tracks']:
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                preview_url = track['preview_url']
                image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                spotify_url = track['external_urls']['spotify']
                
                recommendations.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'preview_url': preview_url,
                    'image_url': image_url,
                    'spotify_url': spotify_url
                })
            
            return recommendations
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return None
    
    def get_top_tracks_by_artist(self, artist_name, limit=5):
        """Get top tracks by an artist"""
        if not self.is_connected():
            return None
        
        try:
            # Search for the artist
            artist_results = self.sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
            if not artist_results['artists']['items']:
                return None
            
            artist_id = artist_results['artists']['items'][0]['id']
            
            # Get top tracks
            top_tracks = self.sp.artist_top_tracks(artist_id)
            
            # Format tracks
            tracks = []
            for track in top_tracks['tracks'][:limit]:
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                preview_url = track['preview_url']
                image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                spotify_url = track['external_urls']['spotify']
                
                tracks.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'preview_url': preview_url,
                    'image_url': image_url,
                    'spotify_url': spotify_url
                })
            
            return tracks
        except Exception as e:
            print(f"Error getting top tracks: {e}")
            return None
    
    def get_related_artists(self, artist_name, limit=5):
        """Get artists related to a given artist"""
        if not self.is_connected():
            return None
        
        try:
            # Search for the artist
            artist_results = self.sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
            if not artist_results['artists']['items']:
                return None
            
            artist_id = artist_results['artists']['items'][0]['id']
            
            # Get related artists
            related = self.sp.artist_related_artists(artist_id)
            
            # Format artists
            artists = []
            for artist in related['artists'][:limit]:
                name = artist['name']
                image_url = artist['images'][0]['url'] if artist['images'] else None
                spotify_url = artist['external_urls']['spotify']
                
                artists.append({
                    'name': name,
                    'image_url': image_url,
                    'spotify_url': spotify_url
                })
            
            return artists
        except Exception as e:
            print(f"Error getting related artists: {e}")
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
    recommender = SpotifyRecommender()
    if recommender.is_connected():
        # Example 1: Get recommendations by mood
        happy_songs = recommender.get_recommendations_by_mood('joy', limit=3)
        print("\nHappy Songs:")
        for song in happy_songs:
            print(f"{song['track_name']} by {song['artist_name']}")
        
        # Example 2: Search for tracks
        search_results = recommender.search_tracks("The Beatles Yesterday", limit=2)
        print("\nSearch Results:")
        for song in search_results:
            print(f"{song['track_name']} by {song['artist_name']}")
        
        # Example 3: Get top tracks by artist
        artist_tracks = recommender.get_top_tracks_by_artist("Queen", limit=2)
        print("\nTop Tracks by Queen:")
        for song in artist_tracks:
            print(f"{song['track_name']}")
    else:
        print("Not connected to Spotify API. Set your credentials in environment variables.")
        print("export SPOTIFY_CLIENT_ID='your_client_id'")
        print("export SPOTIFY_CLIENT_SECRET='your_client_secret'") 