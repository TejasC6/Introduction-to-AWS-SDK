# Program to send message to SQS queue

# Imports
from config import DESIRED_REGION, SQS_QUEUE_NAME, SQS_QUEUE_MESSAGE_GROUP_ID, SQS_QUEUE_MESSAGE_DUPLICATION_ID
from config import sqs_client
from retreive_sqs_queue import retrieve_sqs_queue_url


# Function to send message to SQS queue
def send_message_to_sqs_queue():
    try:
        # Send message to SQS queue
        response = sqs_client.send_message(
            QueueUrl=retrieve_sqs_queue_url(),
            MessageGroupId=SQS_QUEUE_MESSAGE_GROUP_ID,
            MessageDeduplicationId=SQS_QUEUE_MESSAGE_DUPLICATION_ID,
            MessageAttributes={
                'Name': {
                    'DataType': 'String',
                    'StringValue': 'test message'
                }
            },
            MessageBody=(
                'This is a test message'
            ),
        )
        message_id = response['MessageId']
        print(f'\nMessage sent to SQS queue {SQS_QUEUE_NAME} with MessageId: {message_id}')

    except Exception as e:
        print(f'A\nn unexpected error occurred: {e}')


print(f'\nSending message to SQS queue {SQS_QUEUE_NAME} in the region: {DESIRED_REGION}')
print('\nPlease wait for a few seconds')
send_message_to_sqs_queue()  # Call function to send message to SQS
print('\nPlease wait for 30 seconds for SQS queue to be updated')
print('\n')
