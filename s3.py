"""This module has s3 service connection and uploading file into s3"""
import boto3

# import configparser
from botocore.exceptions import ClientError

# config = configparser.ConfigParser()
# config.read('D:/Spotify/credentials.ini')

class S3Service:
    """This class has the methods for s3 service"""
    def __init__(self,bucket_name):
        self.bucket_name = bucket_name
        self.s3_obj = self.s3_connection()

    def s3_connection(self):
        """This function that makes the s3 conncetion"""
        s3_obj = boto3.client(
            "s3",
            aws_access_key_id="AKIAZGSLVELN63NZ6ETB",
            aws_secret_access_key="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",
        )
        return s3_obj

    def upload_file_to_s3(self,file, object_name):
        """This function done the file uploading in s3 aspire-data-dev bucket"""
        status = ""
        try:
            
            s3_obj = self.s3_obj
            bucket_name = self.bucket_name
            s3_obj.upload_file(file,bucket_name,object_name,
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

    def get_file_list(self,bucket_name,prefix):
        """This method used to get the list of files from s3 bucket"""
        s3_obj = self.s3_obj
        file_list = []
        my_bucket = s3_obj.list_objects_v2(Bucket=bucket_name,Prefix=prefix)
        
        for file_obj in my_bucket['Contents']:
            file_list.append(file_obj['Key'])

        return file_list    

    def download_s3file(self,key,dest):
        s3_obj = self.s3_obj
        bucket_name = self.bucket_name
        s3_obj.download_file(bucket_name,'employee/source/employee_details_2021_01_01.json',dest)
        pass

def main():
    aws_s3 = S3Service()
    s3_object = aws_s3.s3_connection()
    print("s3 Connection was Sucessfully done..")

if __name__ == "__main__":
    main()