# import modules
import boto3
from pprint import pprint

# open management console
aws_management_console = boto3.session.Session(profile_name='default')

# open IAM console
# iam_console_resource = aws_management_console.resource('iam')
iam_console_client = aws_management_console.client(service_name='iam')

result = iam_console_client.list_users()
# pprint(result['Users'])
for each_user in result['Users']:
    print(each_user['UserName'])