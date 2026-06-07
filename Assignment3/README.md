Assignment 3: Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3
Objective

Detect S3 buckets that do not have Server-Side Encryption (SSE) enabled.

What is Server-Side Encryption?

When encryption is enabled:

Your File
    ↓
Encrypted before storing in S3
    ↓
Stored securely

Without encryption:

Your File
    ↓
Stored in plain form in S3

AWS recommends enabling encryption for all buckets.

Architecture
AWS Lambda
      |
      v
List All S3 Buckets
      |
      v
Check Encryption Status
      |
      v
Print Unencrypted Buckets
      |
      v
CloudWatch Logs
Step 1: Create Test Buckets

Go to:

AWS Console
→ S3
→ Create Bucket

Create 3 buckets:

encrypted-bucket-1
encrypted-bucket-2
unencrypted-bucket-1

(Use unique names.)

Step 2: Enable Encryption on Some Buckets

Open:

encrypted-bucket-1
→ Properties
→ Default Encryption
→ Edit

Enable:

Server-side encryption with Amazon S3 managed keys (SSE-S3)

Save.

Repeat for:

encrypted-bucket-2

Leave:

unencrypted-bucket-1

without encryption.

Step 3: Create IAM Role

Go to:

IAM
→ Roles
→ Create Role

Choose:

AWS Service
→ Lambda

Click Next.

Attach:

AmazonS3ReadOnlyAccess

Also attach:

AWSLambdaBasicExecutionRole

(Needed for CloudWatch logs.)

Role Name:

LambdaS3EncryptionCheckRole

Click:

Create Role
Why ReadOnly Access?

This assignment only needs to:

List buckets
Check encryption
Print results

No bucket modification is required.

Step 4: Create Lambda Function

Go to:

Lambda
→ Create Function

Choose:

Author from scratch

Function Name:

CheckS3Encryption

Runtime:

Python 3.12

Permissions:

Use Existing Role

Choose:

LambdaS3EncryptionCheckRole

Click:

Create Function
Step 5: Lambda Code

Paste this code:

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
Understanding the Code
Create S3 Client
s3 = boto3.client('s3')

Connects Lambda to Amazon S3.

List All Buckets
buckets = s3.list_buckets()['Buckets']

Example output:

[
 {'Name':'encrypted-bucket-1'},
 {'Name':'encrypted-bucket-2'},
 {'Name':'unencrypted-bucket-1'}
]
Check Encryption
s3.get_bucket_encryption(
    Bucket=bucket_name
)

If encryption exists:

Success

If encryption is absent:

ServerSideEncryptionConfigurationNotFoundError
Store Unencrypted Buckets
unencrypted_buckets.append(bucket_name)

Collects bucket names for reporting.

Step 6: Deploy

Click:

Deploy

Wait for:

Successfully deployed
Step 7: Create Test Event

Click:

Test

Event Name:

check-encryption

Event JSON:

{}

Save.

Step 8: Run Lambda

Click:

Test

Expected output:

{
  "statusCode": 200,
  "unencrypted_buckets": [
      "unencrypted-bucket-1"
  ]
}
Step 9: Check CloudWatch Logs

Go to:

Lambda
→ Monitor
→ View CloudWatch Logs

Open latest log stream.

Expected:

Checking bucket encryption status...

encrypted-bucket-1 : Encryption Enabled

encrypted-bucket-2 : Encryption Enabled

unencrypted-bucket-1 : NOT ENCRYPTED

Unencrypted Buckets:

unencrypted-bucket-1
