# Program to delete all resources: EC2 instances, S3 buckets and SQS queues in specified region

# Imports
from config import DESIRED_REGION, AMI_ID, S3_BUCKET_NAME
from config import ec2_client, s3_client, sqs_client
from delete_objects_in_s3_bucket import delete_all_objects


# Function to delete all instances in specified region
def terminate_all_instances():
    print(f'\nPreparing to terminate all EC2 instances in the region: {DESIRED_REGION}')
    # List all instances
    try:
        all_ec2_response = ec2_client.describe_instances()
        all_ec2_instances = []
        for reservation in all_ec2_response['Reservations']:
            for instance in reservation['Instances']:
                for tag in instance['Tags']:
                    instance_name = tag['Value']
                    all_ec2_instances.append(instance_name)
        print(f'\nBelow is the list of all EC2 instances in region: {DESIRED_REGION} :-')
        for instance in all_ec2_instances:
            print(instance)

        # List only active instances
        active_ec2_response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running', 'pending','stopped'],
                },
                {
                    'Name': 'image-id',
                    'Values': [AMI_ID]

                }
            ]
        )
        # Extract all instance IDs
        instance_ids = []
        instance_names_list = []
        for reservation in active_ec2_response['Reservations']:
            for instance in reservation['Instances']:
                for tag in instance['Tags']:
                    instance_name = tag['Value']
                    print(f'\nPreparing to terminate EC2 instance: {instance_name}')
                    instance_names_list.append(instance_name)
                instance_ids.append(instance['InstanceId'])

        # Check if there are instances to terminate
        if instance_ids:
            # Terminate all instances
            ec2_client.terminate_instances(InstanceIds=instance_ids)
            print(f'\nTerminating instances:')
            for instance in instance_names_list:
                print(instance)
            print(f'\nAll EC2 instances in {DESIRED_REGION} region are terminated successfully')
        else:
            if all_ec2_instances:
                print(f'\nAll instances in region: {DESIRED_REGION} are already terminated')
            else:
                print(f'\nNo active instances found to terminate in region: {DESIRED_REGION}')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')
        

# Function to delete S3 bucket in specified region
def delete_s3_bucket():
    print(f'\nPreparing to delete {S3_BUCKET_NAME} S3 bucket in the region: {DESIRED_REGION}')
    # Delete S3 buckets
    try:
        list_s3_buckets_response = s3_client.list_buckets(
            MaxBuckets=100
        )
        if 'Buckets' in list_s3_buckets_response:
            for bucket in list_s3_buckets_response['Buckets']:
                bucket_name = bucket['Name']
                if bucket_name == S3_BUCKET_NAME:
                    delete_all_objects(bucket_name)
                    s3_client.delete_bucket(Bucket=bucket_name)
                    print(f'\nS3 Bucket {bucket_name} is deleted successfully')
        else:
            print(f'\nNo S3 buckets available in the region {DESIRED_REGION}')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')


"""
# Function to all delete S3 buckets in specified region
def delete_regional_s3_buckets():
    print(f'\nPreparing to delete all S3 buckets in the region: {DESIRED_REGION}')
    # Delete S3 buckets
    try:
        list_s3_buckets_response = s3_client.list_buckets(
            MaxBuckets=100
        )
        regional_bucket_count = 0  # Count of buckets in us-east-1
        if 'Buckets' in list_s3_buckets_response:
            for bucket in list_s3_buckets_response['Buckets']:
                bucket_name = bucket['Name']
                location = s3_client.get_bucket_location(Bucket=bucket_name)
                bucket_region = location['LocationConstraint']
                # S3 is global. Narrow down to specific region
                if bucket_region == DESIRED_REGION:
                    print(f'\nPreparing to delete S3 bucket {bucket_name} in region {DESIRED_REGION}')
                    delete_all_objects(bucket_name)
                    s3_client.delete_bucket(Bucket=bucket_name)
                    print(f'\nS3 Bucket {bucket_name} is deleted successfully')
                    regional_bucket_count += 1
        if regional_bucket_count > 0:
            print(f'\nAll S3 buckets in {DESIRED_REGION} are deleted successfully')
        else:
            print(f'\nNo S3 buckets available in the region {DESIRED_REGION}')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')
"""


# Function to delete all SQS queues in specified region
def delete_all_sqs_queue():
    print(f'\nPreparing to delete all SQS queues in the region: {DESIRED_REGION}')
    # Delete all SQS queues
    try:
        # List all queues in SQS
        list_queue_response = sqs_client.list_queues(
            MaxResults=10
        )
        if 'QueueUrls' in list_queue_response:
            queue_urls = list_queue_response['QueueUrls']
            # Iterate and delete each queue
            for queue_url in queue_urls:
                queue_name = queue_url.split('/')[-1]  # Extract queue name from URL
                print(f'\nPreparing to delete SQS queue {queue_name}')
                sqs_client.delete_queue(QueueUrl=queue_url)
                print(f'\nSQS queue: {queue_name} is deleted successfully')
            print(f'\nAll SQS queues in {DESIRED_REGION} are deleted successfully')
        else:
            print('\nNo queues available in this region')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')


print(f'\nRequests to delete all resources - EC2 instances, S3 buckets and SQS queues in {DESIRED_REGION} have been sent')
print('\nPlease wait for a couple of seconds')
terminate_all_instances()  # Check AWS Console - All EC2 instances in us-east-1 region would be terminated
delete_s3_bucket()  # Check AWS Console - All S3 buckets in us-east-1 region would be deleted
delete_all_sqs_queue()  # Check AWS Console - All SQS queues in us-east-1 region would be deleted
print(f'\nAll resources in {DESIRED_REGION} are deleted successfully')
print('\nPlease wait for 60 seconds before proceeding')
print('\n')
