import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    print("Received Event:")
    print(event)

    # Get instance ID from EventBridge event
    instance_id = event['detail']['instance-id']

    # Current Date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Create Tags
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                'Key': 'LaunchDate',
                'Value': current_date
            },
            {
                'Key': 'Environment',
                'Value': 'Internship'
            }
        ]
    )

    print(f"Successfully tagged instance {instance_id}")

    return {
        'statusCode': 200,
        'body': f'Tagged {instance_id}'
    }
