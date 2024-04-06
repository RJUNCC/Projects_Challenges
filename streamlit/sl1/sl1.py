""" 
Created on Thurday March 28 1:32 AM EST 2024

@author: Ryan Jacobs
"""

#import libs
import pandas as pd
import numpy as np
import streamlit as sm
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import win32com.client
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import requests
import csv

# # load data
# output_dir = Path.cwd() / "Output"
# output_dir.mkdir(parents=True, exist_ok=True)

# # connect to outlook
# outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# # connect to folder
# inbox = outlook.GetDefaultFolder(6)

# # get nessages
# messages = inbox.Items

# for message in messages:
#     subject = message.Subject
#     body = message.body
#     attachments = message.Attachments

#     # create separate folder for each message
#     target_folder = output_dir / str(subject)
#     target_folder.mkdir(parents=True, exist_ok=True)

#     # write body to text file
#     Path(target_folder / "EMAIL_BODY.txt").write_text(str(body))

#     # save attachments
#     for attachment in attachments:
#         attachment.SaveAsFile(target_folder / str(attachment))
    
#     print(body)

# ## CHATGPT
# from exchangelib import Credentials, Account, DELEGATE
# import csv

# def fetch_outlook_emails(username, password, csv_filename):
#     # Connect to Outlook account
#     credentials = Credentials(username=username, password=password)
#     account = Account(primary_smtp_address=username, credentials=credentials, autodiscover=True, access_type=DELEGATE)

#     # Fetch emails
#     emails = account.inbox.all()

#     # Write emails to CSV
#     with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#         fieldnames = ['Subject', 'Sender', 'Date', 'Body']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()

#         for email in emails:
#             writer.writerow({
#                 'Subject': email.subject,
#                 'Sender': str(email.sender),
#                 'Date': email.datetime.strftime("%Y-%m-%d %H:%M:%S"),
#                 'Body': email.text_body
#             })

# if __name__ == "__main__":
#     username = "riainofficial@outlook.com"  # Your Outlook email address
#     password = "NiCeCoCk6969420420!!"  # Your Outlook password
#     csv_filename = "outlook_emails.csv"  # CSV file to store emails
#     fetch_outlook_emails(username, password, csv_filename)

# spam = pd.read_csv()

def get_access_token(client_id, client_secret, tenant_id):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        'client_id': client_id,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Failed to obtain access token")

def fetch_outlook_emails(access_token, csv_filename):
    endpoint = 'https://graph.microsoft.com/v1.0/me/messages'
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(endpoint, headers=headers)
    emails = response.json()['value']

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Subject', 'Sender', 'Date', 'Body']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for email in emails:
            writer.writerow({
                'Subject': email['subject'],
                'Sender': email['sender']['emailAddress']['address'],
                'Date': email['receivedDateTime'],
                'Body': email['body']['content']
            })

if __name__ == "__main__":
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    tenant_id = "your_tenant_id"
    csv_filename = "outlook_emails.csv"

    access_token = get_access_token(client_id, client_secret, tenant_id)
    fetch_outlook_emails(access_token, csv_filename)