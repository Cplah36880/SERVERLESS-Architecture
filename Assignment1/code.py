import boto3

ec2 = boto3.client('ec2')


def lambda_handler(event, context):

    # -------------------------
    # Find Auto-Stop Instances
    # -------------------------

    stop_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Stop']
            }
        ]
    )

    stop_ids = []

    for reservation in stop_response['Reservations']:
        for instance in reservation['Instances']:
            stop_ids.append(instance['InstanceId'])

    if stop_ids:
        ec2.stop_instances(
            InstanceIds=stop_ids
        )

        print("Stopped Instances:")
        for instance in stop_ids:
            print(instance)

    # -------------------------
    # Find Auto-Start Instances
    # -------------------------

    start_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start']
            }
        ]
    )

    start_ids = []

    for reservation in start_response['Reservations']:
        for instance in reservation['Instances']:
            start_ids.append(instance['InstanceId'])

    if start_ids:
        ec2.start_instances(
            InstanceIds=start_ids
        )

        print("Started Instances:")
        for instance in start_ids:
            print(instance)

    return {
        'statusCode': 200,
        'body': 'EC2 automation completed'
    }
