"""This module used for spotify connection and get the playlist response"""
import spotipy
import requests
# import configparser
from spotipy.oauth2 import SpotifyClientCredentials

# config = configparser.ConfigParser()
# config.read('D:/Spotify/credentials.ini')
class SpotifyPlaylist:
    """This class has method for getting playlist from spotify using spotipy api"""

    def spotify_connection(self):
        """This finction that makes the spotify connection"""

        spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id="921a402707bc44eb8769e3de2b4fd30b",
                client_secret="17ed0ad0f91a441397a31d1b5210afac",
            )
        )
        return spotify

    def get_playlist(self,spotify_obj, playlist_id):

        """This function used for get the playlist response"""
        # playlist_uri = 'spotify:playlist:37i9dQZEVXbNG2KDcFcKOF'
        results = ""
        try:
            results = spotify_obj.playlist(playlist_id)
        except spotipy.SpotifyException:
            print("Pass the valid Spotify playlist id in argparse")
        except requests.exceptions.ConnectionError:
            print("Check Your Network Connection")

        return results


# obj = SpotifyPlaylist()
# obj.get_playlist("ds")
