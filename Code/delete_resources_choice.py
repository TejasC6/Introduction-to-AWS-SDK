# Program to delete resources: EC2 instances, S3 buckets and SQS queues in specified region

# Imports
from config import DESIRED_REGION, AMI_ID
from config import ec2_client, s3_client, sqs_client
from delete_objects_in_s3_bucket import delete_all_objects


# Function to terminate EC2 instances
def terminate_ec2_instances():
    try:
        # Lists active EC2 instance and terminates it
        list_ec2_response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running', 'pending', 'stopped'],  # Instance states
                },
                {
                    'Name': 'image-id',
                    'Values': [AMI_ID]

                }
            ]
        )
        if 'Reservations' in list_ec2_response:
            for reservation in list_ec2_response['Reservations']:
                for instance in reservation['Instances']:
                    for tag in instance['Tags']:
                        instance_name = tag['Value']  # Name of EC2 instance
                        instance_id = instance['InstanceId']  # ID of EC2 instance
                        print(f'\nWould you like to delete EC2 instance: {instance_name}')
                        ec2_delete_request = input(
                            '\nWould you like to delete this EC2 instance? Enter Y for YES (Any other '
                            'response to be considered as a NO)\n')
                        if ec2_delete_request == 'Y':
                            ec2_client.terminate_instances(InstanceIds=[instance_id])
                            print(f'\nTerminating EC2 instance: {instance_name}...Please wait')
                            print(f'\nEC2 instance: {instance_name} is deleted successfully')

        else:
            print('\nNo EC2 instances available in this region')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')


# Function to delete S3 buckets
def delete_s3_bucket():
    # Delete S3 buckets
    try:
        list_s3_buckets_response = s3_client.list_buckets(
            MaxBuckets=100
        )
        if 'Buckets' in list_s3_buckets_response:
            for bucket in list_s3_buckets_response['Buckets']:
                bucket_name = bucket['Name']
                location = s3_client.get_bucket_location(Bucket=bucket_name)
                bucket_region = location['LocationConstraint']
                # S3 is global. Narrow down to specific region
                if bucket_region == DESIRED_REGION:
                    print(f'\nWould you like to delete S3 bucket named: {bucket_name}')
                    s3_delete_request = input('\nWould you like to delete this S3 bucket? Enter Y for YES (Any other '
                                              'response to be considered as a NO)\n')
                    if s3_delete_request == 'Y':
                        delete_all_objects(bucket_name)
                        s3_client.delete_bucket(
                            Bucket=bucket_name
                        )
                        print(f'\nS3 Bucket {bucket_name} is deleted successfully')
        else:
            print('\nNo S3 buckets available in this region')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')


# Function to delete SQS queues
def delete_sqs_queue():
    try:
        # List all queues in SQS
        list_queue_response = sqs_client.list_queues(
            MaxResults=10
        )
        if 'QueueUrls' in list_queue_response:
            for queue_url in list_queue_response['QueueUrls']:
                queue_name = queue_url.split('/')[-1]  # Extract queue name from URL
                print(f'\nPreparing to delete SQS queue: {queue_name}')
                sqs_delete_request = input('\nWould you like to delete this SQS queue? Enter Y for YES (Any other '
                                           'response to be considered as a NO)\n')
                if sqs_delete_request == 'Y':
                    sqs_client.delete_queue(
                        QueueUrl=str(queue_url)
                    )
                    print(f'\nSQS Queue {queue_name} is deleted successfully')

        else:
            print('\nNo queues available in this region')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')


print('\nRequests to delete resources - EC2 instances, S3 buckets and SQS queues have been sent')
print('\nPlease wait for a couple of seconds')
terminate_ec2_instances()  # Check AWS Console - selected EC2 instances will be terminated
delete_s3_bucket()  # Check AWS Console - selected S3 buckets will be deleted
delete_sqs_queue()  # Check AWS Console - selected SQS queues will be deleted
print('\nAll required resources are deleted')
print('\nPlease wait for 20 seconds before proceeding')
print('\n')
