"""This module used for spotify connection and get the playlist response"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyPlaylist():
    """This class has method for getting playlist from spotify using spotipy api"""
    def get_playlist(self,playlist_uri):

        """This function used for get the playlist response"""

        id="921a402707bc44eb8769e3de2b4fd30b"
        secret="17ed0ad0f91a441397a31d1b5210afac"

        # playlist_uri = 'spotify:playlist:37i9dQZEVXbNG2KDcFcKOF'

        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=id,
        client_secret=secret,))

        results = spotify.playlist(playlist_uri)
        # results = spotify.playlist_tracks(playlist_uri)["items"]

        return results





