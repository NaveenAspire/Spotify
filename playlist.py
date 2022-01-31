"""This module done the get response from spotify module and make that response as json & csv file the
upoload these files using s3 module"""
import s3,spotify
import argparse
import json,csv
import time

class GetPlaylist():
    """This class has functions for get tracklist and convert the list into json & csv file 
    then upload file"""
    def get_tracklist(self,track_list):
        """function used for get traclist from s3 module"""
        results = spotify.SpotifyPlaylist.get_playlist(self,args.id)
        

        self.playlist_name = results['name']
        # print(playlist_name)
        for track in results['tracks']['items']:
            #Track name
            track_name = track["track"]["name"]
            track_list.append(track_name)
            # print(track_name)
        print(self.playlist_name)
        
        pass
    
    def get_json_playlist(self,track_list):
        """This function make the traclist into json file and upload into s3"""
        epoch_time = str(int(time.time()))
        dest = r"D:\Spotify\Upload/"+epoch_time+".json"

        with open(dest, "w") as file:
            json.dump(track_list, file, indent=4)
        playlist_name = self.playlist_name
        print(playlist_name)

        if playlist_name == "Top Songs - Global":
            s3_file_name = r'Spotify/Source/Top_Songs_Global/top_songs_global_'+epoch_time+'.json'

        if playlist_name == "Top Songs - USA":
            s3_file_name = r'Spotify/Source/Top_Songs_USA/top_songs_usa_'+epoch_time+'.json'

        s3.S3Service.upload_file(self,dest,s3_file_name)    

        pass

    def get_csv_playlist(self,track_list):
        """This function make the traclist into json file and upload into s3"""
        song_list = [
            {'track_name':track_list}
        ]

        fields= ['track_name']
        epoch_time = str(int(time.time()))
        dest = r"D:\Spotify\Upload/"+epoch_time+".csv"

        with open(dest, "w") as file:
            csvwriter = csv.DictWriter(file, fieldnames=fields)
            csvwriter.writeheader()
            csvwriter.writerows(song_list)
        playlist_name = self.playlist_name

        if playlist_name == "Top Songs - Global":
            s3_file_name = r'Spotify/Stage/Top_Songs_Global/top_songs_global_'+epoch_time+'.csv'

        if playlist_name == "Top Songs - USA":
            s3_file_name = r'Spotify/Stage/Top_Songs_USA/top_songs_usa_'+epoch_time+'.csv'

        s3.S3Service.upload_file(self,dest,s3_file_name)
        pass


play = GetPlaylist()

track_list = []
playlist_name = ""

parser = argparse.ArgumentParser()
parser.add_argument('--id', type=str, help='Enter the id for playlist')
args = parser.parse_args()

#Calling get_traclist function for playlist response
play.get_tracklist(track_list)
print(play.playlist_name)

#Calling get_json_playlist function for convert tracklist into json file
play.get_json_playlist(track_list)

#Calling get_json_playlist function for convert tracklist into csv file
play.get_csv_playlist(track_list)

