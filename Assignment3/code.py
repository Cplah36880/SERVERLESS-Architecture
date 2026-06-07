import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):

    print("Checking bucket encryption status...")

    buckets = s3.list_buckets()['Buckets']

    unencrypted_buckets = []

    for bucket in buckets:

        bucket_name = bucket['Name']

        try:
            s3.get_bucket_encryption(
                Bucket=bucket_name
            )

            print(f"{bucket_name} : Encryption Enabled")

        except ClientError as e:

            error_code = e.response['Error']['Code']

            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':

                print(f"{bucket_name} : NOT ENCRYPTED")

                unencrypted_buckets.append(bucket_name)

            else:
                print(f"Error checking {bucket_name}: {e}")

    print("Unencrypted Buckets:")

    for bucket in unencrypted_buckets:
        print(bucket)

    return {
        'statusCode': 200,
        'unencrypted_buckets': unencrypted_buckets
    }
