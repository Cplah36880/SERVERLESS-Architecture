Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

This assignment teaches serverless automation using AWS services:

Amazon S3 → Stores files (objects)
AWS Lambda → Runs code without managing servers
Boto3 → Python SDK used to interact with AWS services
IAM Role → Grants permissions to Lambda
1. Theory: What Are We Building?

Suppose your S3 bucket contains:

File	Upload Date
file1.txt	40 days ago
file2.pdf	35 days ago
file3.jpg	10 days ago
file4.csv	5 days ago

Our Lambda function will:

Check all files in the bucket.
Calculate each file's age.
Delete files older than 30 days.
Keep newer files.
Print deleted filenames in CloudWatch logs.

After execution:

File	Status
file1.txt	Deleted
file2.pdf	Deleted
file3.jpg	Kept
file4.csv	Kept
Architecture
        S3 Bucket
             |
             |
             v
      AWS Lambda
             |
             |
             v
      Boto3 Python Code
             |
             |
             v
 Delete Objects > 30 Days Old
Step 1: Create S3 Bucket
Navigate
AWS Console
   →
S3
   →
Create Bucket
Fill Details

Bucket Name:

cleanup-demo-bucket-12345

(Choose a globally unique name)

Region:

ap-south-1 (Mumbai)

Leave remaining settings as default.

Click:

Create Bucket
Step 2: Upload Files

Open bucket.

Click:

Upload

Upload some files:

sample1.txt
sample2.pdf
sample3.jpg

Click:

Upload
Important Note

You cannot directly change an object's upload date inside S3.

For testing:

Option 1 (Recommended)

Temporarily modify Lambda code to delete files older than:

1 day

instead of

30 days

This allows testing immediately.

Option 2

Use existing old objects if available.

Step 3: Create IAM Role

Lambda needs permission to access S3.

Navigate:

IAM
 →
Roles
 →
Create Role

Select:

AWS Service

Choose:

Lambda

Click:

Next

Search:

AmazonS3FullAccess

Select it.

Also add:

AWSLambdaBasicExecutionRole

This enables CloudWatch logging.

Click:

Next

Role Name:

LambdaS3CleanupRole

Click:

Create Role
Why IAM Role?

Without permissions Lambda cannot:

List bucket contents
Delete objects
Write logs

IAM acts like an access card.

Step 4: Create Lambda Function

Navigate:

AWS Console
 →
Lambda
 →
Create Function

Choose:

Author from Scratch

Function Name:

S3CleanupFunction

Runtime:

Python 3.12

Permissions:

Use Existing Role

Select:

LambdaS3CleanupRole

Click:

Create Function
Step 5: Write Boto3 Code

Delete the default code and paste:

import boto3
from datetime import datetime, timezone, timedelta

# Create S3 client
s3 = boto3.client('s3')

# Bucket name
BUCKET_NAME = 'cleanup-demo-bucket-12345'

def lambda_handler(event, context):

    # Files older than 30 days
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)

    # Get all objects
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("Bucket is empty")
        return

    for obj in response['Contents']:

        key = obj['Key']
        last_modified = obj['LastModified']

        if last_modified < cutoff_date:

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=key
            )

            print(f"Deleted: {key}")

    return {
        'statusCode': 200,
        'body': 'Cleanup completed'
    }
Understanding the Code
Create S3 Client
s3 = boto3.client('s3')

Connects Python code to S3.

Calculate 30-Day Cutoff
cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)

Example:

Today = June 1

Cutoff = May 2

Anything older than May 2 gets deleted.

List Bucket Objects
response = s3.list_objects_v2(
    Bucket=BUCKET_NAME
)

Returns:

{
 'Contents': [
    {
      'Key':'file1.txt',
      'LastModified': ...
    }
 ]
}
Loop Through Files
for obj in response['Contents']:

Checks every file.

Compare Dates
if last_modified < cutoff_date:

Example:

File uploaded: April 1

Cutoff: May 2

April 1 < May 2

Delete File
Delete Object
s3.delete_object(
    Bucket=BUCKET_NAME,
    Key=key
)

Deletes file permanently.

Log Deleted File
print(f"Deleted: {key}")

Appears in CloudWatch logs.

Step 6: Deploy Lambda

Click:

Deploy

Wait until:

Successfully deployed

appears.

Step 7: Manual Invocation

Click:

Test

Create Event:

{}

Event Name:

cleanup-test

Click:

Save

Now click:

Test

again.

Expected output:

{
  "statusCode": 200,
  "body": "Cleanup completed"
}
Step 8: Check Logs

Navigate:

Lambda
 →
Monitor
 →
View CloudWatch Logs

You should see:

Deleted: sample1.txt
Deleted: sample2.pdf

if they were older than 30 days.

Step 9: Verify in S3

Go back to:

S3 Bucket

Refresh bucket.

Expected:

Only files newer than 30 days remain.
