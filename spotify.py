"""This module used for spotify connection and get the playlist response"""
import spotipy
import configparser
from spotipy.oauth2 import SpotifyClientCredentials

config = configparser.ConfigParser()
config.read('D:/Spotify/credentials.ini')


class SpotifyPlaylist:
    """This class has method for getting playlist from spotify using spotipy api"""

    def get_playlist(self, playlist_uri):

        """This function used for get the playlist response"""
        # with open("D:/Spotify/spoti.txt", "r",encoding='utf8') as file:
        #     data = file.readlines()
        #     client_id = data[0].strip("\n")
        #     client_secret = data[1].strip("\n")

        # playlist_uri = 'spotify:playlist:37i9dQZEVXbNG2KDcFcKOF'

        try:
            spotify = spotipy.Spotify(
                client_credentials_manager=SpotifyClientCredentials(
                    client_id=config['spotipy']['client_id'],
                    client_secret=config['spotipy']['client_secret']
                )
            )

            results = spotify.playlist(playlist_uri)
        except spotipy.SpotifyException:
            print("Pass the valid playlist uri id in argparse")
            return False
        # print(results)
        # results = spotify.playlist_tracks(playlist_uri)["items"]

        return results


# obj = SpotifyPlaylist()
# obj.get_playlist("ds")
