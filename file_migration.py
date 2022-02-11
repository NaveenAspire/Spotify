"""This module that download the file from s3 bucket which is not in anoter bucket
then upload into second bucket"""
import argparse
import os
import logging
import s3

logging.basicConfig(level=logging.INFO)
log_path = os.path.join(os.path.dirname(os.getcwd()),'opt/log/file_migration/')
if not os.path.exists(log_path):
    os.makedirs(log_path)
log_file =  os.path.join(log_path,"file_migration_logging.log")
logging.basicConfig(
    filename=log_file,
    datefmt="%d-%b-%y %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    force=True,
)

class S3FileMigration:
    """This class is has methods for migrate the files from one s3 bucket to another"""

    def __init__(self, source_bucket, target_bucket):
        """This is the init method for class S3FileMigration"""
        self.source_bucket = source_bucket
        self.target_bucket = target_bucket
        self.local_dest = os.path.join(
            os.path.dirname(os.getcwd()), "opt/data/file_migration"
        )
        if not os.path.exists(self.local_dest):
            os.makedirs(self.local_dest)

    def migrate_files(self):
        """This function transfer the s3 files from one bucket to another"""
        logging.info("migrate file method is called.")
        self.download_unuploaded_files()
        s3_sevice = s3.S3Service("aspire-data-dev")
        for file in os.listdir(self.local_dest):
            if ".json" in file:
                s3_sevice.upload_file_to_s3(
                    self.local_dest + "/" + str(file), "employee/source/" + str(file)
                )

    def download_unuploaded_files(self):
        """This function download the s3 files which not in another bucket"""
        files_list = self.get_unuploaded_files()
        logging.info("Sucessfully get the unploaded files of target bucket as list.")
        s3_service = s3.S3Service("aspire-employee-dev")
        dest = self.local_dest
        for file in files_list:
            key = file.split("/")[-1]
            s3_service.download_s3file(file, dest + "/" + key)
        logging.info("Sucessfully downloaded the unploaded files of target bucket.")

    def get_unuploaded_files(self):
        logging.info("download unploaded method is called.")
        s3_service = s3.S3Service("aspire-employee-dev")
        source_bucket_files = s3_service.get_file_list(
            "aspire-employee-dev", "employee/source/"
        )
        logging.info("Sucessfully get the souce bucket files as list.")
        target_bucket_files = s3_service.get_file_list(
            "aspire-data-dev", "employee/source/"
        )
        logging.info("Sucessfully get the target bucket files as list.")
        files_list = [
            file for file in source_bucket_files if file not in target_bucket_files
        ]
        return files_list

def main():
    """This is the main function for the module"""
    parser = argparse.ArgumentParser(description="For file migration between s3 buckets")
    parser.add_argument("--source_bucket",type=str,
        help="Enter the source bucket name of s3",required=True,
    )
    parser.add_argument("--target_bucket",type=str,
        help="Enter the target bucket name of s3",required=True,
    )
    args = parser.parse_args()
    s3_file_migrate = S3FileMigration(args.source_bucket, args.target_bucket)
    s3_file_migrate.migrate_files()

if __name__ == "__main__":
    main()
