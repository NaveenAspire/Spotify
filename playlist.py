"""This module done the get response from spotify module and make that 
response as json & csv file theupoload these files using s3 module"""
import argparse
import json
import csv
import time
import logging
import s3
import spotify

logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    filename="D:/Spotify/spotify_logging.log",
    datefmt="%d-%b-%y %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    force=True,
)


class GetPlaylist:
    """This class has functions for get tracklist and convert the list into json & csv file
    then upload file"""

    def get_tracklist(self, track_list):
        """function used for get traclist from s3 module"""
        logging.info("Calling the get_palylist method from spotify module")
        results = spotify.SpotifyPlaylist.get_playlist(self, args.id)
        if not results:
            logging.error("There is no response from get_playlist methd")
            return False
        logging.info("Sucessfully get playlist response from spotify")
        self.playlist_name = results["name"]
        # print(playlist_name)
        for track in results["tracks"]["items"]:
            # Track name
            track_name = track["track"]["name"]
            track_list.append(track_name)
            # print(track_name)
        logging.info("Sucessfully get tracklist names")
        print(self.playlist_name)

        self.get_json_playlist(track_list)

        self.get_csv_playlist(track_list)

    def get_json_playlist(self, track_list):
        """This function make the traclist into json file and upload into s3"""
        epoch_time = str(int(time.time()))
        dest = r"D:\Spotify\Upload/" + epoch_time + ".json"

        with open(dest, "w") as file:
            json.dump(track_list, file, indent=4)
        logging.info("Sucessfully created json file for playlist")
        playlist_name = self.playlist_name
        # print(playlist_name)

        if playlist_name == "Top Songs - Global":
            s3_file_name = (
                r"Spotify/Source/Top_Songs_Global/top_songs_global_"
                + epoch_time
                + ".json"
            )

        elif playlist_name == "Top Songs - USA":
            s3_file_name = (
                r"Spotify/Source/Top_Songs_USA/top_songs_usa_" + epoch_time + ".json"
            )
        else:
            print("Wrong Playlist")
            logging.error(
                "json playlist file not uploded in s3 bucket due to wrong playlist"
            )
            return

        s3.S3Service.upload_file(self, dest, s3_file_name)
        logging.info("Sucessfully json playlist uploaded into s3 bucket")

        pass

    def get_csv_playlist(self, track_list):
        """This function make the traclist into json file and upload into s3"""
        song_list = [{"track_name": track_list}]

        fields = ["track_name"]
        epoch_time = str(int(time.time()))
        dest = r"D:\Spotify\Upload/" + epoch_time + ".csv"

        with open(dest, "w", encoding="utf8") as file:
            csvwriter = csv.DictWriter(file, fieldnames=fields)
            csvwriter.writeheader()
            csvwriter.writerows(song_list)
        logging.info("Sucessfully created csv file for playlist")
        playlist_name = self.playlist_name

        if playlist_name == "Top Songs - Global":
            s3_file_name = (
                r"Spotify/Stage/Top_Songs_Global/top_songs_global_"
                + epoch_time
                + ".csv"
            )

        elif playlist_name == "Top Songs - USA":
            s3_file_name = (
                r"Spotify/Stage/Top_Songs_USA/top_songs_usa_" + epoch_time + ".csv"
            )
        else:
            print("Wrong Playlist")
            logging.error("csv file not uploded in s3 bucket due to wrong playlist")
            return
        s3.S3Service.upload_file(self, dest, s3_file_name)
        logging.info("Sucessfully csv playlist file uploaded into s3 bucket")
        
play = GetPlaylist()

track_list = []
playlist_name = ""

parser = argparse.ArgumentParser()
parser.add_argument("--id", type=str, help="Enter the id for playlist", required=True)
args = parser.parse_args()

# Calling get_traclist function for playlist response
play.get_tracklist(track_list)
# print(play.playlist_name)

# Calling get_json_playlist function for convert tracklist into json file
# play.get_json_playlist(track_list)

# Calling get_json_playlist function for convert tracklist into csv file
# play.get_csv_playlist(track_list)
