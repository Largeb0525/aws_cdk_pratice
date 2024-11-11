import json
import os
import boto3
from botocore.exceptions import ClientError

sqs = boto3.client('sqs')
queue_url = os.environ['QUEUE_URL']


def main(event, context):
    if event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        try:
            sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Message sent to SQS'})
            }
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    elif event['httpMethod'] == 'GET':
        try:
            messages = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=2
            )
            if 'Messages' in messages:
                message = messages['Messages'][0]
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
                return {
                    'statusCode': 200,
                    'body': message['Body']
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'No messages in queue'})
                }
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method not allowed'})
        }
