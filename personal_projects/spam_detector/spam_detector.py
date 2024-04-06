import csv
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm 

# FILENAME_1 = 'mail.mbox'
# FILENAME_2 = 'mail2.mbx'
# EMAIL_1 = 'Emails.csv'
# def email_to_csv(FILENAME: str, EMAIL_NAME: str):
#     # read file
#     mboxFile = open(FILENAME, encoding="utf8")

#     emails = {}
#     for line in mboxFile:
#         if "From:" in line:
#             email = re.findall(r'[\w\.-]+@[\w\.-]+', line)
#             if len(email) > 0:
#                 if email[0] in emails:
#                     emails[email[0]] += 1
#                 else:
#                     emails.update({email[0]: 1})
#     mboxFile.close()

#     # Output to CSV
#     field_names = ['Email', 'Count']
#     with open('Emails.csv', 'w') as f:
#         writer = csv.DictWriter(f, fieldnames=field_names)
#         writer.writeheader()
#         for key in emails:
#             writer.writerow({'Email': key, 'Count': emails[key]})

spam = pd.read_csv('spam.csv')

X = spam['v2']
y = spam['v1']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# ramdomly assigns a number to each word in a process called tokenizing, then counts number of occurences of words 
cv = CountVectorizer()
features = cv.fit_transform(X_train)

# build model
svc = svm.SVC()
svc.fit(features, y_train)

# testing email spam detector
features_test = cv.transform(X_test)
print(f"Accuracy: {svc.score(features_test, y_test)}")