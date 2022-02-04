"""This module done the get response from spotify module and make that
response as json & csv file theupoload these files using s3 module"""
import argparse
import time
import logging
import os
import pandas as pd
import s3
import spotify

logging.basicConfig(level=logging.INFO)
log_file = os.path.dirname(os.getcwd()) + "/spotify_logging.log"
logging.basicConfig(
    filename=log_file,
    datefmt="%d-%b-%y %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    force=True,
)

class GetPlaylist:
    """This class has functions for get tracklist and convert the list into json & csv file
    then upload file"""

    def get_tracklist(self, spotify_obj, id):
        """function used for get traclist from s3 module"""
        logging.info("Calling the get_palylist method from spotify module")
        results = spotify.SpotifyPlaylist.get_playlist(self,spotify_obj, id)
        data_as_df = ""
        playlist_name = ""
        if results:
            logging.info("Sucessfully get playlist response from spotify")
            track_list = []
            album_list = []
            duration_list = []
            date_list = []
            playlist_name = results["name"]
            for track in results["tracks"]["items"]:
                track_name = track["track"]["name"]
                track_list.append(track_name)
                album_name = track["track"]["album"]["name"]
                ms = track["track"]["duration_ms"]
                ss, ms = divmod(ms, 1000)
                mm, ss = divmod(ss, 60)
                date_added = track["added_at"]
                album_list.append(album_name)
                duration_list.append(str(mm) + ":" + str(ss))
                date_list.append(date_added)
            logging.info("Sucessfully get tracklist names")
            data = {
                "Title": track_list,
                "Album": album_list,
                "Duration": duration_list,
                "Date Added": date_list,
            }
            data_as_df = pd.DataFrame(data)
        return data_as_df, playlist_name

    def get_jsonfile_from_df(self, s3_obj, df_playlist, playlist_name):
        """This function make the traclist into json file and upload into s3"""
        json_file = (
            playlist_name.replace(" - ", "_").lower().replace(" ", "_")
            + "_"
            + str(int(time.time()))
        )
        path = os.getcwd()
        path = os.path.dirname(path)
        dest = path+"/"+(json_file) + ".json"
        df_playlist.to_json(dest, orient="records", indent=4)
        s3_file_name = r"Spotify/Source/" + playlist_name + "/" + json_file + ".json"
        s3.S3Service.upload_file_to_s3(self,s3_obj, dest, s3_file_name)
        logging.info("Sucessfully json playlist uploaded into s3 bucket")

    def get_csvfile_from_df(self, s3_obj, df_playlist, playlist_name):
        """This function make the traclist into csv file and upload into s3"""
        csv_file = (
            playlist_name.replace(" - ", "_").lower().replace(" ", "_")
            + "_"
            + str(int(time.time()))
        )
        path = os.getcwd()
        path = os.path.dirname(path)
        dest = path+"/"+(csv_file) + ".csv"
        df_playlist.to_csv(dest, index=False)

        s3_file_name = r"Spotify/Stage/" + playlist_name + "/" + csv_file + ".csv"
        s3.S3Service.upload_file_to_s3(self,s3_obj, dest, s3_file_name)
        logging.info("Sucessfully json playlist uploaded into s3 bucket")

def main():
    """This is the main function of the module"""
    play = GetPlaylist()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--id", type=str, help="Enter the id for playlist", required=True
    )
    args = parser.parse_args()
    s3_obj = s3.S3Service.s3_connection(play)
    spotify_obj = spotify.SpotifyPlaylist.spotify_connection(play)
    try:
        df_playlist, playlist_name = play.get_tracklist(spotify_obj, args.id)
        if playlist_name:
            play.get_jsonfile_from_df(s3_obj, df_playlist, playlist_name)
            play.get_csvfile_from_df(s3_obj, df_playlist, playlist_name)
    except TypeError as error:
        print(error)


if __name__ == "__main__":
    main()
