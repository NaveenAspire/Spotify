import s3
import argparse


class S3FileMigration :
    """This class is has methods for migrate the files from one s3 bucket to another"""
    def __init__(self,source_bucket,target_bucket):
        """This is the init method for class S3FileMigration"""
        self.source_bucket = source_bucket
        self.target_bucket = target_bucket


    def migrate_files(self):
        unuploded_files = self.download_unuploaded_files()
        pass

    def download_unuploaded_files(self):
        s3_service = s3.S3Service("aspire-employee-dev")
        source_bucket_files = s3_service.get_file_list('aspire-employee-dev','employee/source/')
        target_bucket_files = s3_service.get_file_list('aspire-data-dev','employee/source/')
        files_list = [file for file in source_bucket_files if file not in target_bucket_files]
        for file in files_list:
            s3_service.download_s3file(file,'D:/Spotify/emp_details.json')

        pass

def main():
    parser = argparse.ArgumentParser(description="For file migration between s3 buckets")
    parser.add_argument("--source_bucket", type=str,help="Enter the source bucket name of s3",required=True)
    parser.add_argument("--target_bucket", type=str,help="Enter the target bucket name of s3",required=True)
    args = parser.parse_args()
    s3_file_migrate = S3FileMigration(args.source_bucket,args.target_bucket)
    s3_file_migrate.migrate_files()
    

if __name__ == '__main__':
    main()