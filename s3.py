"""This module has s3 service connection and uploading file into s3"""
import boto3

# import configparser
from botocore.exceptions import ClientError

# config = configparser.ConfigParser()
# config.read('D:/Spotify/credentials.ini')

class S3Service:
    """This class has the methods for s3 service"""

    def s3_connection(self):
        """This function that makes the s3 conncetion"""
        s3_obj = boto3.client(
            "s3",
            aws_access_key_id="AKIAZGSLVELN63NZ6ETB",
            aws_secret_access_key="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",
        )
        return s3_obj

    def upload_file_to_s3(self,s3_obj, file, object_name):
        """This function done the file uploading in s3 aspire-data-dev bucket"""
        status = ""
        try:
            bucket_name = "aspire-data-dev"
            s3_obj.upload_file(
                file,
                bucket_name,
                object_name,
                ExtraArgs={"ACL": "public-read"},
            )
            status = "Updated Sucessfully"
        except ClientError as error:
            print(error)
        except boto3.exceptions.S3UploadFailedError as error:
            # print(error)
            status = "Invaid Access key Id or Secret Access Key Id was given in aws s3 connection"
            print(status)
        return status
