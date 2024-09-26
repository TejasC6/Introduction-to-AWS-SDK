# Program to create all 3 resources: AWS EC2 Instance, S3 Bucket and SQS Queue

# Imports
from config import DESIRED_REGION, AMI_ID, EC2_INSTANCE_NAME, S3_BUCKET_NAME, SQS_QUEUE_NAME
from config import ec2_client, s3_client, sqs_client

# Set local file path to create new file
local_file_path = (r'D:\\ASU\\Fall 24\\Courses\\CSE 546 Cloud Computing by Yuli Deng\\'
                   r'Project 1 - AWS Basics\\')


# Function to create and run EC2 instance
def create_ec_instance():
    # Step 1: Create a Key Pair with the name "Tejas"
    try:
        key_pair_response = ec2_client.create_key_pair(KeyName='Tejas')
        print(f'\nCreated key pair for EC2 with name: {key_pair_response['KeyName']}')
        # Save the private key to a file
        with open(local_file_path + 'Tejas.pem', 'w') as key_file:
            key_file.write(key_pair_response['KeyMaterial'])
        print('Key saved as "Tejas.pem". Remember to keep it secure.')
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}\n')

    try:
        # Creates EC2 instance
        print('\nCreating EC2 instance')
        ec2_client.run_instances(
            ImageId=AMI_ID,
            KeyName='Tejas',
            MinCount=1,  # Number of instances
            MaxCount=1,
            InstanceType='t2.micro',  # Free tier
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',  # Provide name to EC2 instance
                            'Value': EC2_INSTANCE_NAME  # EC2 instance name
                        }
                    ]
                }
            ]
        )
        print(f'\nEC2 instance {EC2_INSTANCE_NAME} created successfully in the region: {DESIRED_REGION}\n')
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}\n')


# Function to create a new S3 bucket in specified region
def create_s3_bucket():
    try:
        # Create S3 bucket
        print('\nCreating S3 bucket')
        s3_client.create_bucket(
            Bucket=S3_BUCKET_NAME
        )
        print(f'\nS3 bucket: {S3_BUCKET_NAME} created successfully in the region: {s3_client.meta.region_name}\n')

    # Cannot use same name for 2 S3 buckets in your account
    except s3_client.exceptions.BucketAlreadyExists:
        print(f'\nError: The bucket name {S3_BUCKET_NAME} is already taken. Choose a unique name.\n')
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}\n')


# Function to create a new SQS Queue in specified region
def create_sqs_queue():
    try:
        # Create SQS Queue
        print('\nCreating SQS queue')
        sqs_client.create_queue(
            QueueName=SQS_QUEUE_NAME,
            Attributes={'FifoQueue': 'true'}
        )
        print(f'\nSQS queue: {SQS_QUEUE_NAME} created successfully in the region: {DESIRED_REGION}\n')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}\n')


print('\nRequests to create resources - 1 EC2 instance, 1 S3 bucket and 1 SQS queue have been sent')
print('\nPlease wait for 1 minute and check AWS Console\n')
create_ec_instance()  # Check AWS Console - New EC2 instance will be initializing
create_s3_bucket()  # Check AWS Console - New S3 bucket will be created
create_sqs_queue()  # Check AWS Console - New SQS queue will be created
print('\nPlease wait for 1 minute')
