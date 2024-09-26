# Program to delete all objects inside an S3 bucket

# Cannot delete bucket if it contains objects in it

# Imports
from config import s3_client


# Function to delete all objects in the bucket
def delete_all_objects(bucket):
    # List objects in the bucket
    objects = s3_client.list_objects_v2(Bucket=bucket)

    # Check if the bucket has any objects
    if 'Contents' in objects:
        # Extract object keys
        object_keys = [{'Key': obj['Key']} for obj in objects['Contents']]

        # Delete all objects
        s3_client.delete_objects(Bucket=bucket, Delete={'Objects': object_keys})
        print(f'\nDeleted all objects in the bucket: {bucket}')
    else:
        print(f'\nNo objects found in the bucket: {bucket}')
