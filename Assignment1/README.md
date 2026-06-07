Assignment 1: Automated EC2 Instance Management Using AWS Lambda and Boto3

This assignment teaches serverless automation in AWS using Lambda, Boto3, IAM, and EC2.

1. Understanding the Concept
What is AWS Lambda?

AWS Lambda is a serverless computing service that runs your code without managing servers.

Instead of:

Creating a server
Installing Python
Running scripts manually

AWS executes your code automatically whenever you trigger it.

Benefits
No server management
Pay only when code runs
Easy automation of AWS resources
What is Boto3?

Boto3 is the official Python SDK for AWS.

It allows Python code to interact with AWS services.

Example:

import boto3

ec2 = boto3.client('ec2')

Now Python can:

Start EC2 instances
Stop EC2 instances
Create S3 buckets
Manage IAM users

and much more.

Why Use Tags?

Tags help identify resources.

Example:

Resource	Tag Key	Tag Value
EC2 Instance 1	Action	Auto-Stop
EC2 Instance 2	Action	Auto-Start

Our Lambda function will:

Find instances tagged Auto-Stop
Stop them

and

Find instances tagged Auto-Start
Start them
Architecture
             Lambda Function
                    |
                    |
               Boto3 SDK
                    |
       -------------------------
       |                       |
EC2 Instance 1           EC2 Instance 2
(Action=Auto-Stop)      (Action=Auto-Start)

       Stop                    Start
Step 1: Create Two EC2 Instances
Login

Open:

AWS Console

Go to:

Services → EC2
Launch Instance 1

Click:

Launch Instance

Settings:

Name: Stop-Instance

AMI:
Amazon Linux 2023

Instance Type:
t2.micro

Key Pair:
Create or select existing

Security Group:
Allow SSH

Click:

Launch Instance
Launch Instance 2

Again click:

Launch Instance

Settings:

Name: Start-Instance

AMI:
Amazon Linux 2023

Instance Type:
t2.micro

Click:

Launch Instance
Step 2: Add Tags

Go to:

EC2 Dashboard → Instances
Tag First Instance

Select:

Stop-Instance

Choose:

Actions
→ Instance Settings
→ Manage Tags

Add:

Key = Action
Value = Auto-Stop

Save.

Tag Second Instance

Select:

Start-Instance

Add:

Key = Action
Value = Auto-Start

Save.

Step 3: Create IAM Role
Why IAM Role?

Lambda cannot access EC2 unless permissions are granted.

IAM Role acts like an identity card.

Navigate:

IAM → Roles

Click:

Create Role
Trusted Entity

Choose:

AWS Service

Service:

Lambda

Next.

Attach Permission

Search:

AmazonEC2FullAccess

Select it.

Next.

Role Name:

LambdaEC2ManagerRole

Create Role.

Step 4: Create Lambda Function

Navigate:

AWS Lambda

Click:

Create Function

Select:

Author from Scratch

Function Name:

EC2AutoManager

Runtime:

Python 3.13

Execution Role:

Use Existing Role

Choose:

LambdaEC2ManagerRole

Create Function.

Step 5: Understanding the Boto3 Logic

The Lambda will:

First

Find instances:

Action = Auto-Stop

using:

describe_instances()
Second

Stop them:

stop_instances()
Third

Find instances:

Action = Auto-Start
Fourth

Start them:

start_instances()
Step 6: Write Lambda Code

Replace default code with:

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
Code Explanation
Create EC2 Client
ec2 = boto3.client('ec2')

Connects Lambda to EC2 service.

Describe Instances
describe_instances()

Fetches EC2 information.

Filter by Tag
Filters=[
{
'Name':'tag:Action',
'Values':['Auto-Stop']
}
]

Means:

Find all instances where

Tag Key = Action
Tag Value = Auto-Stop
Collect Instance IDs
stop_ids.append(instance['InstanceId'])

Example:

i-0abc12345xyz

Stored for stopping.

Stop Instances
ec2.stop_instances(
InstanceIds=stop_ids
)

Stops all matching instances.

Start Instances
ec2.start_instances(
InstanceIds=start_ids
)

Starts all matching instances.

Step 7: Deploy the Function

Click:

Deploy

Wait until:

Successfully deployed

appears.

Step 8: Create Test Event

Click:

Test

Create Event.

Name:

TestEvent

JSON:

{}

Save.

Step 9: Invoke Lambda

Click:

Test

Lambda executes immediately.

Expected output:

Stopped Instances:
i-xxxxxxxx

Started Instances:
i-yyyyyyyy
Step 10: Verify Results

Go to:

EC2 Dashboard → Instances

Observe:

Instance 1
Action = Auto-Stop

State should become:

Stopping
→ Stopped
Instance 2
Action = Auto-Start

State should become:

Pending
→ Running
Viewing Logs

Lambda automatically stores logs in:

Amazon CloudWatch

Navigate:

Lambda
→ Monitor
→ View CloudWatch Logs

You can see:

Started Instances:
i-xxxxxxx

Stopped Instances:
i-yyyyyyy
