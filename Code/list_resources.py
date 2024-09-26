# Program to list resources: EC2 instances, S3 buckets and SQS queues in specified region

# Imports
from config import DESIRED_REGION, AMI_ID, S3_BUCKET_NAME
from config import ec2_client, s3_client, sqs_client


# Function to list all EC2 instances in specified region
def list_ec2_instances():
    try:
        # Lists active EC2 instances
        print(f'\nReading list of EC2 instances in the region: {DESIRED_REGION}')
        print(f'\nBelow is a list of all EC2 instances in the region: {DESIRED_REGION}')
        list_ec2_response = ec2_client.describe_instances()
        if 'Reservations' in list_ec2_response and list_ec2_response['Reservations'] != []:
            # To extract the name of each instance
            for reservation in list_ec2_response['Reservations']:
                for instance in reservation['Instances']:
                    for tag in instance['Tags']:
                        print(tag['Value'])

            print(f'\nBelow is a list of all ***ACTIVE*** EC2 instances in the region: {DESIRED_REGION}')
            # List only active EC2 instances
            list_active_ec2_response = ec2_client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': ['running', 'pending'],
                        # Does not include instances with states - stopping, stopped, terminated, shutting down
                    },
                    {
                        'Name': 'image-id',
                        'Values': [AMI_ID]

                    }
                ]
            )
            if 'Reservations' in list_active_ec2_response and list_active_ec2_response['Reservations'] != []:
                # To extract the name of each instance
                for reservation in list_active_ec2_response['Reservations']:
                    for instance in reservation['Instances']:
                        for tag in instance['Tags']:
                            print(tag['Value'])

            else:
                print('No active EC2 instances available in this region')
        else:
            print('No EC2 instances present in this region')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}\n')


# Function to list all S3 buckets
def list_s3_buckets():
    # List all S3 buckets in AWS account
    try:
        """
        # Code to list of all S3 buckets in your AWS account:
        print('\nBelow is a list of all S3 buckets in your ***AWS account***:')  # S3 is Global
        list_all_s3_buckets_response = s3_client.list_buckets()
        if 'Buckets' in list_all_s3_buckets_response:
            for bucket in list_all_s3_buckets_response['Buckets']:
                bucket_name = bucket['Name']
                print(bucket_name)
        """
        # Code to list S3 buckets based on region - does not work for us-east-1
        print(f'\nBelow is a list of S3 buckets in the region: {DESIRED_REGION}')
        # List S3 buckets only if they are present in us-east-1 region
        list_s3_buckets_response = s3_client.list_buckets(
            MaxBuckets=100
        )
        
        regional_bucket_count = 0  # Count of buckets in us-east-1
        if 'Buckets' in list_s3_buckets_response:
            for bucket in list_s3_buckets_response['Buckets']:
                bucket_name = bucket['Name']
                location = s3_client.get_bucket_location(Bucket=bucket_name)
                bucket_region = location['LocationConstraint']
                if bucket_region == DESIRED_REGION:  # For S3 buckets other DESIRED_REGION in general
                    print(bucket_name)
                    regional_bucket_count += 1
                elif bucket_region is None:  # For S3 buckets in us-east-1 region
                    print(bucket_name)
                    regional_bucket_count += 1

        if regional_bucket_count == 0:
            print('No S3 buckets present in this region')

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Function to list SQS queues
def list_sqs_queues():
    # List SQS queues
    try:
        print(f'\nReading list of SQS queues in the region: {DESIRED_REGION}')
        list_sqs_queues_response = sqs_client.list_queues(
            MaxResults=10
        )
        print(f'\nBelow is a list of SQS queues in the region: {DESIRED_REGION}')
        if 'QueueUrls' in list_sqs_queues_response:
            for queue_url in list_sqs_queues_response['QueueUrls']:
                print(queue_url.split('/')[-1])  # Extracts queue name from queue URL
        else:
            print('No queues available in this region')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')


print('\nRequests to list resources - EC2 instances, S3 buckets and SQS queues have been sent')
print('\nPlease wait for a couple of seconds')
list_ec2_instances()  # Output a list of EC2 instances
list_s3_buckets()  # Output a list of S3 buckets
list_sqs_queues()  # Output a list of SQS queues
print('\n')
