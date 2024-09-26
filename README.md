#### Name: Tejas Chandrasekhar
#### ASU ID: 1233415172
#### Course: CSE 546 'Cloud Computing' by Yuli Deng, ASU Fall '24


# YouTube video Link:
```
https://youtu.be/hvhBPwr8-c8
```

# Instructions to run this application

## Prerequisites:
1. Download and install PyCharm or any apt IDE
2. Download and install Python
3. Install boto3 (AWS SDK) package in PyCharm or via command prompt
4. Create AWS account and have access to AWS Management Console

## Steps to run the application:
1. Once AWS account is setup, you need to generate Access Key ID and Secret Access Key
   - Suggestion: Instead of generating Access Key ID for root user, create an IAM user with basic/required access permissions and generate Access Key ID for the IAM user.
2. Configure PyCharm Project Terminal to connect with AWS
   - Create new project in PyCharm and make sure the project is configured to Python Script package and boto3 library is installed
   - Open PyCharm project terminal and run the command- ```aws configure```
   - This command requests you to provide the Access Key ID, Secret Access Key (previously generated), default region and default output format
   - You do not have to provide AWS Secret Key and Access Key ID each time during boto3 client initialization
   - Provide required details. For this project, I have used us-east-1 N.Virginia as default region
3. Run the run_application.py in the PyCharm terminal using the command below. This file simply runs all other files in the project in order. The other files as explained in the next sections.
```
python run_application.py
```

### NOTE: 
Common files in the project's .zip file i.e., files imported by 2 or more main files of the project - help reduce redundant code
1. config.py - this file contains code to import boto3, initializing all commonly used variables and initializing all commonly used boto3 clients
   - Avoids importing boto3 and initializing variables and boto3 clients multiple times
   - Other files can simply import config file and its attributes
2. delete_objects_in_s3 - this file contains code to delete all objects in a specified S3 bucket
   - S3 buckets cannot be directly deleted through boto3 if they contain objects inside them
   - This file deletes objects in the S3 bucket and thus helps in deleting the S3 bucket itself
3. retrieve_sqs_queue.py - this file contains code to retrieve the queue URL of the SQS queue created for this project
   - Returns SQS Queue URL of the SQS queue created - useful in multiple actions performed on SQS queues like sending messages, counting number of messages and receiving messages 

## Project Description and Procedure:
1. Load the AWS SDK(you may use whatever language you prefer, as long as there is an AWS SDK available)
   - Procedure: Completed in previous steps
2. Read your access information, to be able to access AWS service (Guidance of how to get access information like access key ID, token and session key are included in the AWS Introduction ppt that was shared with you earlier.)
   - Procedure: Completed in previous steps
3. Send resource request API call to AWS to create the EC2 instance, S3 bucket, and SQS queue.
   - Procedure: Run the create_resources.py file
     - Creates EC2 instance, S3 bucket and SQS queue based on information provided in the config file
4. Wait for 1 min.
   - Procedure: Printed out apt message within create_resources.py file
5. List all EC2 instances, S3 buckets, and SQS queues in your accounts in the current region again, print them out.
   - Procedure: Run the list_resources.py file
     - Lists all the EC2 instances, S3 buckets and SQS queues in the region us-east-1
6. Upload an empty text file with the name “CSE546test.txt” into the S3 bucket that you just created.
   - Procedure: Run the upload_file_to_s3.py file
     - Creates an empty text file named 'CSE546test.txt' in a specified local file path
     - Uploads this text file to specified S3 bucket (the S3 bucket created in previous steps)
7. Send a message with the message name “test message” and message body “This is a test message” into the SQS queue.
   - Procedure: Run the send_message_sqs.py file
     - Sends a message to the SQS queue created with the specified Title and Body
8. Check how many messages are there in your SQS queue, print it out in a new line.
   - Procedure: Run the count_messages_sqs_queue.py file
     - Counts the number of messages in the SQS queue created
9. Pull the message you just sent from the SQS queue, print out the message title and body in two lines.
   - Procedure: Run the pull_message_from_sqs_queue.py file
     - Retrieves message from SQS queue created, prints out the Title and Body of the message and provides user a choice to delete the message from the SQS queue
10. Check how many messages are there in your SQS queue again.
    - Procedure: Run the count_messages_sqs_queue.py file again.
      - This time, the count should be lower if user deletes the message in previous step
11. Wait for 10 seconds.
    - Procedure: Printed out apt message within pull_message_from_sqs_queue.py and count_messages_sqs_queue.py files
12. Delete all the resources.
    - Procedure: Provided two options for this step:
      1. Run the delete_all_resources.py file
         - This file simply deletes all resources that exist in the specified region i.e., us-east-1
      2. Run the delete_resources_choice.py file
         - This file lists each resource i.e., each EC2 instance, S3 bucket and SQS queue in the us-east-1 region and asks the user whether the user wants to delete the resource, one at a time
         - Provides user flexibility to choose not to delete resources that we created outside of this project
13. Wait for 20 seconds.
    - Procedure: Printed out apt message within delete_all_resources.py and delete_resources_choice.py files
14. List all EC2 instances, S3 buckets, and SQS queues in your accounts in the current region again.
    - Procedure: Run the list_resources.py file again
      - This time, the count of resources should be lower as some/all of them were deleted in the previous step
15. Also, print out a message each time an action is done.
    - Procedure: Printed out apt messages after each action in all the files discussed earlier

# Output of the application run:
```

Requests to create resources - 1 EC2 instance, 1 S3 bucket and 1 SQS queue have been
 sent

Please wait for 1 minute and check AWS Console


Created key pair for EC2 with name: Tejas
Key saved as "Tejas.pem". Remember to keep it secure.

Creating EC2 instance

EC2 instance cse546_project1_worker created successfully in the region: us-east-1   


Creating S3 bucket

S3 bucket: cse546-project1-bucket created successfully in the region: us-east-1     


Creating SQS queue

SQS queue: cse546_project1_queue.fifo created successfully in the region: us-east-1 


Please wait for 1 minute

Requests to list resources - EC2 instances, S3 buckets and SQS queues have been sent

Please wait for a couple of seconds

Reading list of EC2 instances in the region: us-east-1

Below is a list of all EC2 instances in the region: us-east-1
cse546_project1_worker

Below is a list of all ***ACTIVE*** EC2 instances in the region: us-east-1
cse546_project1_worker

Below is a list of S3 buckets in the region: us-east-1
cse546-project1-bucket

Reading list of SQS queues in the region: us-east-1

Below is a list of SQS queues in the region: us-east-1
cse546_project1_queue.fifo



Preparing to upload file from local to AWS S3

Empty .txt file named CSE546test.txt is successfully created in D:\\ASU\\Fall 24\\Co
urses\\CSE 546 Cloud Computing by Yuli Deng\\Project 1 - AWS Basics\\CSE546test.txt 

Preparing to upload file to S3

Please wait for a few seconds

File CSE546test.txt is uploaded to S3 bucket cse546-project1-bucket



Sending message to SQS queue cse546_project1_queue.fifo in the region: us-east-1    

Please wait for a few seconds

Message sent to SQS queue cse546_project1_queue.fifo with MessageId: 62c39653-e638-4
5df-9563-a27fa63d23bf

Please wait for 30 seconds for SQS queue to be updated



Reading messages in SQS queue: cse546_project1_queue.fifo

Approximate number of messages in SQS queue cse546_project1_queue.fifo is 1

Please wait for 10 seconds for SQS queue to be updated



Retrieving messages from SQS queue: cse546_project1_queue.fifo

Message Details:
Name: test message
Body: This is a test message

Would you like to delete this message?
Enter Y for YES or N for NO: Y

Message deleted successfully.

Please wait for 30 seconds for SQS queue to be updated



Reading messages in SQS queue: cse546_project1_queue.fifo

Approximate number of messages in SQS queue cse546_project1_queue.fifo is 0

Please wait for 10 seconds for SQS queue to be updated



Requests to delete all resources - EC2 instances, S3 buckets and SQS queues in us-ea
st-1 have been sent

Please wait for a couple of seconds

Preparing to terminate all EC2 instances in the region: us-east-1

Below is the list of all EC2 instances in region: us-east-1 :-
cse546_project1_worker

Preparing to terminate EC2 instance: cse546_project1_worker

Terminating instances:
cse546_project1_worker

All EC2 instances in us-east-1 region are terminated successfully

Preparing to delete cse546-project1-bucket S3 bucket in the region: us-east-1       

Deleted all objects in the bucket: cse546-project1-bucket

S3 Bucket cse546-project1-bucket is deleted successfully

Preparing to delete all SQS queues in the region: us-east-1

Preparing to delete SQS queue cse546_project1_queue.fifo

SQS queue: cse546_project1_queue.fifo is deleted successfully

All SQS queues in us-east-1 are deleted successfully

All resources in us-east-1 are deleted successfully

Please wait for 60 seconds before proceeding



Requests to list resources - EC2 instances, S3 buckets and SQS queues have been sent

Please wait for a couple of seconds

Reading list of EC2 instances in the region: us-east-1

Below is a list of all EC2 instances in the region: us-east-1
cse546_project1_worker

Below is a list of all ***ACTIVE*** EC2 instances in the region: us-east-1
No active EC2 instances available in this region

Below is a list of S3 buckets in the region: us-east-1
No S3 buckets present in this region

Reading list of SQS queues in the region: us-east-1

Below is a list of SQS queues in the region: us-east-1
No queues available in this region


```


### Thank you.