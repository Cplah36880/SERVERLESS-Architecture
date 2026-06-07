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
