#%%
import requests
from requests import post, get
from dotenv import load_dotenv
import os
import base64
import json
import streamlit as st
from pprint import pprint
# import hashlib
# import secrets
# from flask import Flask, redirect, request
# import Express
import string
from functions import *

#%%
client_id, client_secret = load_env()
rURI = "https://open.spotify.com/artist/0AyhSYrWjcI7Z0n5SGrqmY"
unique_state = "392"
auth_url = "https://accounts.spotify.com/authorize?client_id=14ad40b2678d4e9b84b42b92b78b2d19&response_type=code&redirect_uri=https://open.spotify.com/artist/0AyhSYrWjcI7Z0n5SGrqmY&scope=user-library-read%20user-read-private%20user-read-email&state=392"

#%% Generate code_verifier once
code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

#%%
print("Please open the following URL in a browser to authorize:")
print(auth_url)

# manually enter auth code obtained from teh redirect URL
auth_code = input("Enter auth code: ")

#%%
token_response = exchange_code_for_token(auth_code, code_verifier, client_id, client_secret, rURI)
print(token_response)

#%%
token = token_response['access_token']
headers = {
    'Authorization':"Bearer " + token
}
print(token, headers)

#%%
user_saved_tracks = get_user_saved_tracks(token, None, headers)

list_of_dicts = []
for idx, i in enumerate(user_saved_tracks['items']):
    big_dict = {}
    big_dict[i['track']['name']] = [{'artist_info':[{'name':{}}], 'album_name':set([i['track']['album']['name']]), 'album_URI':set([i['track']['album']['uri']])}]
    for artist in i['track']['artists']:
        big_dict[i['track']['name']][0]['artist_info'][0]['name'][artist['name']] = artist['id']
        # big_dict[i['track']['name']][0]['artist_info'][0]['name'][artist['name']] = artist['id']
        # print(temp_dict)
        # print(idx)
        # print(artist)
    list_of_dicts.append(big_dict)
pprint(list_of_dicts)

#%%


#%%
    # print(f"{i['track']['name']} by {i['track']['artists']['name']}")
# token = get_token()
# # token = json.loads(response.content.decode('utf-8'))['access_token']
# # headers = {
# #     'Authorization': 'Bearer ' + token
# # }
# # result = get_artist_id(token, 'Tool')
# # artist_id = result['id']
# # songs = get_songs_by_artist(token, artist_id)
# tracks = get_user_saved_tracks(token)
# print(token)
# # print(headers)
# print(tracks)

# related = related_artists(token, artist_id)
# for idx, artist in enumerate(related):
#     print(f"{idx + 1}. {artist['name']}")

# for idx, song in enumerate(songs):
#     print(f"{idx + 1}. {song['name']}")

# for idx, song in enumerate(tracks):
#     print(f"{idx + 1}. {song['name']}")
# print(tracks)

# # streamlit app title
# st.title("Spotify App - Top 10 Tracks")

# # text input
# artist_name = st.text_input("Enter artist name: ")

# if st.button("Search"):
#     if artist_name:
#         token = get_token()
#         artist_info = get_artist_id(token, artist_name)
#         artist_id = artist_info['id']
        
#         if artist_info:
            
#             # col1, col2, col3 = st.columns(3)
#             col1, col2 = st.columns(2)
#             col3, col4 = st.columns(2)
#             with col1:
#                 st.header(f"Top Tracks by {artist_name}")
#                 songs = get_songs_by_artist(token, artist_info['id'])
#                 for idx, song in enumerate(songs):
#                     # st.write(f"{idx + 1}. {song['name']}")
#                     st.write(f"{idx + 1}. [{song['name']}](https://open.spotify.com/track/{song['id']})")
#             with col2:
#                 st.header(f"Artists related to {artist_name}")
#                 related = related_artists(token, artist_id)
#                 for idx, artist in enumerate(related):
#                     if idx == 10:
#                         break
#                     # st.write(f"{idx + 1}. {artist['name']}")
#                     st.write(f"{idx + 1}. [{artist['name']}](https://open.spotify.com/artist/{artist['id']})")
#             # with col3:
#                 # st.header("Shows: ")
#                 # shows = get_artist_shows(token, artist_id)
#                 # for show in shows:
#                 #     st.write(f"{show['date']} - {show['venue']['name']}, {show['venue']['city']['name']}, {show['venue']['country']}")
#                 # st.header("Playback menu: ")
#                 # st.write("Click link to play on Spotify")
#             with col3:
#                 st.header("Recommended Tracks")
            
#             with col4:
#                 st.header("")
#         else:
#             st.write("No artist with this name exists...")
#     else:
#         st.write("Please enter an artist name.")

