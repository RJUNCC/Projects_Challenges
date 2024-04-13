import requests
import pandas as pd
import time

API_KEY = "AIzaSyCu6vnThruOwlHj52XH9ESumQnD6LVJdv4"
CHANNEL_ID = "UCo_LnYpsLfu0t0f-FTzZaAQ"

# make api call
url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000"
response = requests.get(url).json()

print(response['items'][0]['id'])