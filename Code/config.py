# Program to initialize variables

# Imports
import boto3

# Initializing constants
DESIRED_REGION = 'us-east-1'
AMI_ID = 'ami-0ebfd941bbafe70c6'  # Ubuntu Server 24.04 LTS - Free Tier in us-east-1 region
EC2_INSTANCE_NAME = 'cse546_project1_worker'  # Give a name to EC2 Instance to be created
S3_BUCKET_NAME = 'cse546-project1-bucket'  # Give a name to S3 Bucket to be created
SQS_QUEUE_NAME = 'cse546_project1_queue.fifo'  # Give a name to SQS Queue to be created
SQS_QUEUE_MESSAGE_GROUP_ID = 'fifo_group_1'  # Give a group id to SQS message for FIFO queue
SQS_QUEUE_MESSAGE_DUPLICATION_ID = 'fifo_message_duplication_id'  # Give a message duplication ID for FIFO queue message

# Initializing boto3 clients
ec2_client = boto3.client('ec2', region_name=DESIRED_REGION)
s3_client = boto3.client('s3', region_name=DESIRED_REGION)
sqs_client = boto3.client('sqs', region_name=DESIRED_REGION)
