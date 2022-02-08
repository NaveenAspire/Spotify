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
        data_as_df = playlist_name = ""
        if results:
            logging.info("Sucessfully get playlist response from spotify")
            playlist_name = results["name"]
            items = results["tracks"]["items"]
            data_as_df = self.get_dataframe(items)
        return data_as_df, playlist_name

    def get_dataframe(self,items):
        """This function makes the response as data frame"""
        track_details,column_list = ([] for i in range(2) )
        for track in items:
            track_details.append(track['track'])
        for key in items[0]['track'].keys():
            column_list.append(key)
        logging.info("Sucessfully get track details from spotify")
        data_as_df = pd.DataFrame(track_details, columns=column_list,)
        return data_as_df

    def get_jsonfile_from_df(self, s3_obj, df_playlist, playlist_name):
        """This function make the traclist into json file and upload into s3"""
        json_file = (playlist_name.replace(" - ", "_").lower().replace(" ", "_")+ "_"
            + str(int(time.time())))
        path = os.path.dirname(os.getcwd())
        dest = path+"/"+(json_file) + ".json"
        df_playlist.to_json(dest, orient = 'records',lines = True)
        s3_file_name = r"Spotify/Source/" + playlist_name + "/" + json_file + ".json"
        status = s3.S3Service.upload_file_to_s3(self,s3_obj, dest, s3_file_name)
        if status != "Updated Sucessfully":
            logging.error(status)
        logging.info("Sucessfully json playlist uploaded into s3 bucket")

    def get_csvfile_from_df(self, s3_obj, df_playlist, playlist_name):
        """This function make the traclist into csv file and upload into s3"""
        csv_file = (playlist_name.replace(" - ", "_").lower().replace(" ", "_")+ "_"
            + str(int(time.time())))
        path = os.path.dirname(os.getcwd())
        dest = path+"/"+(csv_file) + ".csv"
        df_playlist.to_csv(dest, index=False)
        s3_file_name = r"Spotify/Stage/" + playlist_name + "/" + csv_file + ".csv"
        status = s3.S3Service.upload_file_to_s3(self,s3_obj, dest, s3_file_name)
        if status != "Updated Sucessfully" :
            logging.error(status)
        logging.info("Sucessfully csv playlist uploaded into s3 bucket")

def main():
    """This is the main function of the module"""
    play = GetPlaylist()
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=str, help="Enter the id for playlist", required=True)
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
