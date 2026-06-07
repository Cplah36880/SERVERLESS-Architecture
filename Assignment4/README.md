Assignment 4: Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3
Objective
Automatically:
Create snapshots of an EBS volume.
Delete snapshots older than 30 days.
Save storage costs by removing old backups.

Theory
What is an EBS Volume?
An EBS Volume is a virtual hard disk attached to an EC2 instance.
Example:
EC2 Instance
     |
     |
     V
EBS Volume (100 GB)
All your application data is stored inside the EBS volume.

What is a Snapshot?
A Snapshot is a backup of an EBS volume stored in Amazon S3.
EBS Volume
     |
Create Snapshot
     |
     V
Snapshot Backup
If the volume is lost:
Snapshot
     |
Restore
     |
     V
New EBS Volume

Architecture
CloudWatch Event
       |
       V
AWS Lambda
       |
       +---- Create Snapshot
       |
       +---- Delete Old Snapshots
       |
       V
CloudWatch Logs

Step 1: Identify EBS Volume
Go to:
AWS Console
→ EC2
→ Elastic Block Store
→ Volumes
You will see:
vol-0123456789abcdef0
Copy the Volume ID.
Example:
vol-0a1b2c3d4e5f67890

If No Volume Exists
Create one.
Go to:
EC2
→ Volumes
→ Create Volume
Settings:
Volume Type : gp3
Size        : 5 GB
AZ          : Same as your EC2
Click:
Create Volume

Step 2: Create IAM Role
Go to:
IAM
→ Roles
→ Create Role
Choose:
AWS Service
→ Lambda
Attach:
AmazonEC2FullAccess
Also attach:
AWSLambdaBasicExecutionRole
Role Name:
LambdaEBSSnapshotRole
Click:
Create Role

Why These Permissions?
Lambda needs permission to:
Create snapshots
List snapshots
Delete snapshots
Write logs

Step 3: Create Lambda Function
Go to:
Lambda
→ Create Function
Choose:
Author from Scratch
Function Name:
EBSSnapshotCleanup
Runtime:
Python 3.12
Execution Role:
Use Existing Role
Select:
LambdaEBSSnapshotRole
Click:
Create Function

Step 4: Lambda Code
Replace:
import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

# Replace with your volume ID
VOLUME_ID = 'vol-0a1b2c3d4e5f67890'

def lambda_handler(event, context):

   print("Starting snapshot process")

   # Create Snapshot
   snapshot = ec2.create_snapshot(
       VolumeId=VOLUME_ID,
       Description='Automated Lambda Snapshot'
   )

   snapshot_id = snapshot['SnapshotId']

   print(f"Created Snapshot: {snapshot_id}")

   # Calculate cutoff date
   cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)

   # List snapshots owned by account
   snapshots = ec2.describe_snapshots(
       OwnerIds=['self']
   )

   # Delete old snapshots
   for snap in snapshots['Snapshots']:

       start_time = snap['StartTime']

       if start_time < cutoff_date:

           old_snapshot_id = snap['SnapshotId']

           ec2.delete_snapshot(
               SnapshotId=old_snapshot_id
           )

           print(f"Deleted Snapshot: {old_snapshot_id}")

   return {
       'statusCode': 200,
       'body': f'Created Snapshot: {snapshot_id}'
   }

Step 5: Update Volume ID
Replace:
VOLUME_ID = 'vol-0a1b2c3d4e5f67890'
with your actual Volume ID:
VOLUME_ID = 'vol-xxxxxxxxxxxxx'

Step 6: Deploy
Click:
Deploy
Wait for:
Successfully deployed

Step 7: Create Test Event
Click:
Test
Event Name:
snapshot-test
Event JSON:
{}
Save.

Step 8: Execute Lambda
Click:
Test
Expected result:
{
 "statusCode": 200,
 "body": "Created Snapshot: snap-xxxxxxxx"
}

Step 9: Verify Snapshot
Go to:
EC2
→ Elastic Block Store
→ Snapshots
You should see:
snap-xxxxxxxx
Status:
Pending
After a few minutes:
Completed

Step 10: Check Logs
Go to:
Lambda
→ Monitor
→ View CloudWatch Logs
Latest log stream:
Expected:
Starting snapshot process

Created Snapshot: snap-0123456789

Deleted Snapshot: snap-0987654321

FINAL CODE FOR LAMBDA:

Python code
import boto3
from datetime import datetime, timezone, timedelta

# Create EC2 client
ec2 = boto3.client('ec2')

# Replace with your EBS Volume ID
VOLUME_ID = 'vol-xxxxxxxxxxxxxxxxx'

def lambda_handler(event, context):

    print("Starting snapshot process")

    # Create a new snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated Lambda Snapshot'
    )

    snapshot_id = snapshot['SnapshotId']

    print(f"Created Snapshot: {snapshot_id}")

    # For assignment submission use days=30
    # For testing use minutes=5 or minutes=7

    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=7)

    # Get all snapshots owned by this account
    snapshots = ec2.describe_snapshots(
        OwnerIds=['self']
    )

    for snap in snapshots['Snapshots']:

        start_time = snap['StartTime']
        old_snapshot_id = snap['SnapshotId']

        # Only process snapshots created by this Lambda
        if snap.get('Description') != 'Automated Lambda Snapshot':
            continue

        if start_time < cutoff_date:

            try:
                ec2.delete_snapshot(
                    SnapshotId=old_snapshot_id
                )

                print(f"Deleted Snapshot: {old_snapshot_id}")

            except Exception as e:
                print(
                    f"Could not delete {old_snapshot_id}: {str(e)}"
                )

    return {
        'statusCode': 200,
        'body': f'Created Snapshot: {snapshot_id}'
    }


