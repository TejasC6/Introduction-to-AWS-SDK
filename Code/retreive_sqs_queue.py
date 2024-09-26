# Program to retrieve required SQS queue

# Imports
from config import SQS_QUEUE_NAME, sqs_client


# Function to retrieve required SQS queue
def retrieve_sqs_queue_url():
    sqs_queue_url=''
    try:
        # List queues in SQS
        list_sqs_queues_response = sqs_client.list_queues(
            MaxResults=10
        )
        if 'QueueUrls' in list_sqs_queues_response:
            for queue_url in list_sqs_queues_response['QueueUrls']:
                if queue_url.split('/')[-1] == SQS_QUEUE_NAME:
                    sqs_queue_url = queue_url
        else:
            print('\nNo queues available\n')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}\n')

    return sqs_queue_url
