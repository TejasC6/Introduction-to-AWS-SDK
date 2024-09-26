# Program to upload file to S3 bucket

# Imports
from config import S3_BUCKET_NAME
from config import s3_client
import os

# Set local file path to create new file
local_file_path = (r'D:\\ASU\\Fall 24\\Courses\\CSE 546 Cloud Computing by Yuli Deng\\'
                   r'Project 1 - AWS Basics\\CSE546test.txt')
local_file_name = local_file_path.split('\\')[-1]

print('\nPreparing to upload file from local to AWS S3')
with open(local_file_path, 'w') as file:
    pass
print(f'\nEmpty .txt file named {local_file_name} is successfully created in {local_file_path}')


# Function to upload file to S3
def upload_file_to_s3(file_path, bucket, object_name=None):
    if object_name is None:
        object_name = file_path
    else:
        object_name = local_file_name

    try:
        # Upload file to S3
        s3_client.upload_file(file_path, bucket, object_name)
        print(f'\nFile {object_name} is uploaded to S3 bucket {bucket}')
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')


print('\nPreparing to upload file to S3')
print('\nPlease wait for a few seconds')
upload_file_to_s3(local_file_path, S3_BUCKET_NAME, local_file_name)
print('\n')
