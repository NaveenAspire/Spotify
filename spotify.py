"""This module used for spotify connection and get the playlist response"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyPlaylist():
    """This class has method for getting playlist from spotify using spotipy api"""
    def get_playlist(self,playlist_uri):

        """This function used for get the playlist response"""
        with open("D:\Spotify/spoti.txt", "r") as file:
            data = file.readlines()
            id = data[0].strip("\n")
            secret = data[1].strip("\n")

        print(id)

        # playlist_uri = 'spotify:playlist:37i9dQZEVXbNG2KDcFcKOF'

        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=id,
        client_secret=secret,))

        results = spotify.playlist(playlist_uri)
        print(results)
        # results = spotify.playlist_tracks(playlist_uri)["items"]

        return results

# obj = SpotifyPlaylist()
# obj.get_playlist("ds")



