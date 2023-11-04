import re

# get the text after the @ symbol using regex
def afterAt(ls: list) -> list:
    return [re.search(r'@[\w.]+', i).group()[1:] for i in ls]

clients = ['brucewayne@gotham.com', 'homer_simpson@springfieldnuclear.com', 'hank_hill@arlenpropane.com', 'petergriffin@pawtucketbrewery.com']

print(afterAt(clients))
# print([re.search(r'[\w.]+@', i).group()[:-1] for i in clients])
