# Imports
import subprocess
import time

subprocess.run("create_resources.py", shell=True)
time.sleep(60)
subprocess.run("list_resources.py", shell=True)
subprocess.run("upload_file_to_s3.py", shell=True)
subprocess.run("send_message_sqs.py", shell=True)
time.sleep(30)  # 30s is required for SQS queue to be updated and to get an accurate count
subprocess.run("count_messages_sqs_queue.py", shell=True)
time.sleep(10)
subprocess.run("pull_message_from_sqs_queue.py", shell=True)
time.sleep(30)  # 30s is required for SQS queue to be updated and to get an accurate count and 20s is not enough
subprocess.run("count_messages_sqs_queue.py", shell=True)
time.sleep(10)
subprocess.run("delete_all_resources.py", shell=True)
time.sleep(60)  # 60s is required for SQS queue to be updated and to get an accurate and 30s is not enough
subprocess.run("list_resources.py", shell=True)
