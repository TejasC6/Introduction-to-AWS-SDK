# Program to count number of messages in SQS queue

# Imports
from config import sqs_client, SQS_QUEUE_NAME
from retreive_sqs_queue import retrieve_sqs_queue_url


# Function to count messages in SQS queue
def count_messages_in_sqs_queue():
    try:
        # Count messages in SQS queue
        response = sqs_client.get_queue_attributes(
            QueueUrl=retrieve_sqs_queue_url(),
            AttributeNames=['ApproximateNumberOfMessages']
        )
        # Extract the number of messages
        num_messages = int(response['Attributes'].get('ApproximateNumberOfMessages', 0))
        print(f"\nApproximate number of messages in SQS queue {SQS_QUEUE_NAME} is {num_messages}")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


print(f'\nReading messages in SQS queue: {SQS_QUEUE_NAME}')
count_messages_in_sqs_queue()  # Outputs number of messages in specified SQS queue
print('\nPlease wait for 10 seconds for SQS queue to be updated')
print('\n')
