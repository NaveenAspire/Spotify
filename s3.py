"""This module has s3 service connection and uploading file into s3"""
import boto3
import configparser
from botocore.exceptions import ClientError

config = configparser.ConfigParser()
config.read('D:/Spotify/credentials.ini')

class S3Service:
    """This class has the methods for s3 service"""
    def upload_file(self, file, object_name):
        """This function done the file uploading in s3 aspire-data-dev bucket"""
        try:
            bucket_name = "aspire-data-dev"
            s3.upload_file(
                file,
                bucket_name,
                object_name,
                ExtraArgs={"ACL": "public-read"},
            )
        except ClientError:
            pass


# with open("D:/PythonExplore/access.txt", "r",encoding="utf8") as acess:
#     data = acess.readlines()
#     aws_acess_key = data[0].strip("\n")
#     aws_secret_key = data[1].strip("\n")
s3 = boto3.client(
    "s3", aws_access_key_id= config['aws']['aws_acess_key'],
    aws_secret_access_key= config['aws']['aws_secret_key']
)

