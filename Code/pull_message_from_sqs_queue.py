# Program to pull messages from specific SQS queue

# Imports
from config import sqs_client, SQS_QUEUE_NAME
from retreive_sqs_queue import retrieve_sqs_queue_url


# Function to request user input to delete message
def choice_of_user(message=None):
    delete_token = input('\nWould you like to delete this message? \nEnter Y for YES or N for NO: ')
    if delete_token == 'Y':
        # After processing the message, delete it from the queue
        sqs_client.delete_message(
            QueueUrl=retrieve_sqs_queue_url(),
            ReceiptHandle=message['ReceiptHandle']
        )
        print('\nMessage deleted successfully.')
    elif delete_token == 'N':
        print('\nMessage not deleted')
    else:
        print('\nYou must choose between Y or N')
        return choice_of_user()


# Function to pull messages from specified SQS queue
def pull_message():
    try:
        # Receive messages from SQS queue
        response = sqs_client.receive_message(
            QueueUrl=retrieve_sqs_queue_url(),
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10,
            VisibilityTimeout=100
        )
        # Check for messages in response
        if 'Messages' in response:
            for message in response['Messages']:
                message_title = message['MessageAttributes']['Name']['StringValue']
                message_body = message['Body']
                print(f'\nMessage Details:\nName: {message_title} \nBody: {message_body}')
                choice_of_user(message)  # User's choice to delete message
        else:
            print(f'\nNo messages available in SQS queue: {SQS_QUEUE_NAME}')

    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')


print(f'\nRetrieving messages from SQS queue: {SQS_QUEUE_NAME}')
pull_message()  # Outputs list of messages in the SQS queue
print('\nPlease wait for 30 seconds for SQS queue to be updated')
print('\n')
