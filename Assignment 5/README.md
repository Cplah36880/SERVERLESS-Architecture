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

Step 1: Add Triggering Event
On the left side, click:
AWS SERVICE EVENTS
Then select:
EC2
You should see EC2-related events.
Choose:
EC2 Instance State-change Notification
Drag it (or click the + button) into the Triggering Events box in the middle.

Step 2: Configure the Event
After adding the EC2 event, set:
State = running
This means:
Whenever an EC2 instance enters RUNNING state
→ EventBridge triggers Lambda

Step 3: Add Target
In the Targets box on the right:
Click the + icon or drag a target.
Choose:
AWS Service
Then:
Lambda Function
Select your Lambda function:
AutoTagEC2

Step 4: Configure Rule
Click the Configure tab (next to Build).
Enter:
Rule Name:
EC2LaunchTaggingRule
Ensure:
State: Enabled

Step 5: Create Rule
Click:
Create
(top-right button)

Now do this:
Step 1: Click "Event pattern (Filter)"
In the middle box, click the blue button:
Event pattern (Filter)
that is visible below:
EC2 Instance State-change Notification

Step 2: Add a Filter
A configuration panel should open.
Look for something related to:
state
or
detail.state
Select:
running
only.
If AWS shows a JSON editor, use:
{
 "detail": {
   "state": ["running"]
 }
}

Step 3: Add Lambda Target
After configuring the filter:
Click the + icon inside the Targets box on the right.
Choose:
AWS Service
Then:
Lambda Function
Select your Lambda:
AutoTagEC2

Step 4: Configure Rule
Click the Configure tab at the top (next to Build).
Enter:
Rule Name:
EC2LaunchTaggingRule
Keep:
Event Bus: default
State: Enabled

Step 5: Create
Click the orange:
Create
button.
Do this:
Click on state (the underlined word on the left side under detail).
A popup opens (similar to the one currently showing "type": "string").
Replace the contents with:
[
 "running"
]
or if AWS expects an object:
{
 "equals": ["running"]
}
Click Apply or Save in that popup.

Even easier
In the Event pattern (filter) box on the right, replace the current pattern with:
{
 "source": ["aws.ec2"],
 "detail-type": ["EC2 Instance State-change Notification"],
 "detail": {
   "state": ["running"]
 }
}
This explicitly tells EventBridge:
Only trigger when an EC2 instance reaches the RUNNING state.
After that:
Click Targets tab on the left.
Add target → Lambda Function.
Select your AutoTagEC2 Lambda.
Click Configure.
Set Rule Name:
EC2LaunchTaggingRule
Click Create.
Now perform the final test
1. Verify Lambda is attached as the target
Go to:
EventBridge
→ Rules
→ EC2LaunchTaggingRule
Check that under Targets you see:
AutoTagEC2
(or whatever your Lambda function name is).

2. Launch a new EC2 instance
Go to:
EC2
→ Instances
→ Launch Instance
Create a small test instance (t2.micro/t3.micro).
Wait until the instance state becomes:
Running

3. Wait 1–2 minutes
EventBridge triggers asynchronously, so give AWS a minute or two.

4. Check Tags
Open the newly launched instance.
Go to:
Tags
You should see something like:
Key
Value
LaunchDate
2026-06-07
Environment
Internship

(or whatever tags your Lambda code creates).

5. Check CloudWatch Logs
Go to:
Lambda
→ AutoTagEC2
→ Monitor
→ View CloudWatch Logs
You should see messages such as:
Received Event
Tagged instance i-xxxxxxxxxxxx


