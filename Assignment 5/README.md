Assignment 5: Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3

Automatically add tags to every newly launched EC2 instance.
Example:
When an EC2 instance is launched:
Name = AutoTaggedInstance
LaunchDate = 2026-06-07
Environment = Internship
These tags help in:
Resource management
Cost tracking
Security auditing
Instance identification

Architecture
Launch EC2 Instance
        │
        ▼
EventBridge Rule
        │
        ▼
Lambda Function
        │
        ▼
Add Tags to EC2
        │
        ▼
CloudWatch Logs

Step 1: Create IAM Role
Go to:
IAM
→ Roles
→ Create Role
Choose:
AWS Service
→ Lambda
Attach policies:
AmazonEC2FullAccess
AWSLambdaBasicExecutionRole
Role Name:
LambdaEC2TaggingRole
Click:
Create Role

Step 2: Create Lambda Function
Go to:
Lambda
→ Create Function
Choose:
Author From Scratch
Function Name:
AutoTagEC2
Runtime:
Python 3.12
Execution Role:
Use Existing Role
Select:
LambdaEC2TaggingRole
Click:
Create Function

Step 3: Lambda Code
Replace the default code with:
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

Understanding the Code
Create EC2 Client
ec2 = boto3.client('ec2')
Allows Lambda to communicate with EC2.

Read Instance ID
EventBridge sends:
{
 "detail": {
   "instance-id": "i-0123456789abcdef"
 }
}
Lambda extracts:
instance_id = event['detail']['instance-id']

Generate Current Date
current_date = datetime.now().strftime("%Y-%m-%d")
Example:
2026-06-07

Create Tags
ec2.create_tags(...)
Adds:
LaunchDate = 2026-06-07
Environment = Internship

Step 4: Deploy
Click:
Deploy
Wait until:
Successfully deployed
appears.

Step 5: Create EventBridge Rule
Go to:
Amazon EventBridge
→ Rules
→ Create Rule
Rule Name:
EC2LaunchTaggingRule
Rule Type:
Rule with an Event Pattern

Event Source
Choose:
AWS Events or EventBridge Partner Events

Event Pattern
Choose:
AWS Service
Service:
EC2
Event Type:
EC2 Instance State-change Notification
Specific State:
running
This means:
Whenever an EC2 instance enters RUNNING state
→ Trigger Lambda

Step 6: Add Target
Target Type:
AWS Service
Target:
Lambda Function
Select:
AutoTagEC2
Click:
Create Rule

Step 7: Grant Permissions
EventBridge usually asks:
Allow EventBridge to invoke Lambda?
Choose:
Allow
AWS automatically creates:
lambda:InvokeFunction
permission.

Step 8: Testing
Launch a new EC2 instance.
Go to:
EC2
→ Instances
→ Launch Instance
Choose:
Amazon Linux 2023
t2.micro / t3.micro
Launch.
Wait:
1-2 minutes
until status becomes:
Running

Step 9: Verify Tags
Open the instance.
Go to:
Tags Tab
You should see:
Key
Value
LaunchDate
2026-06-07
Environment
Internship


Step 10: Verify CloudWatch Logs
Go to:
Lambda
→ AutoTagEC2
→ Monitor
→ View CloudWatch Logs
Expected:
Received Event

Successfully tagged instance i-1234567890abcdef
