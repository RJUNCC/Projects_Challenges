import boto3

# open management console
aws_management_console = boto3.session.Session(profile_name='default')

# open EC2 console
ec2_console_client = aws_management_console.client('ec2')

# 
result = ec2_console_client.describe_instances()
print(result)