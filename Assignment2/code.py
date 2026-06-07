import boto3
from datetime import datetime, timezone, timedelta

# Create S3 client
s3 = boto3.client('s3')

# Replace with your bucket name
BUCKET_NAME = 'your-bucket-name'

def lambda_handler(event, context):

    print("Lambda started")

    # Files older than 7 minutes
    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=7)

    # List objects in bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("Bucket is empty")
        return {
            'statusCode': 200,
            'body': 'Bucket is empty'
        }

    for obj in response['Contents']:

        key = obj['Key']
        last_modified = obj['LastModified']

        print(f"Found file: {key}")
        print(f"Last Modified: {last_modified}")

        if last_modified < cutoff_date:

            print(f"Deleting: {key}")

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=key
            )

            print(f"Deleted: {key}")

    return {
        'statusCode': 200,
        'body': 'Cleanup completed successfully'
    }
