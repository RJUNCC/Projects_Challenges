import requests
from requests import post, get
from dotenv import load_dotenv
import os
import base64
import json
import streamlit as st

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# INIT
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":"Basic " + auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }

    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {"Authorization":"Bearer " + token}


# SEARCH
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    # query = f"q={artist_name}&type=artist,track"
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    # print(json_result)
    return json_result

# def search_show(token, artist_name):
#     url = f"https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     query = f"?q={artist_name}&type=artist,show&limit=5"
#     query_url = url+query
#     result = get(query_url, headers=headers)
#     json_result = json.loads(result.content)
#     print(json_result)


# GET
def get_artist_id(token, artist_name):
    json_result = search_for_artist(token, artist_name)['artists']['items']
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result[0]

# def get_show_id(token, artist_name):
#     json_result = search_show(token, artist_name)['shows']

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    # print(result)
    json_result = json.loads(result.content)['tracks']
    return json_result

def related_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['artists']
    return json_result

# def get_new_releases(token, artist_id):
#     url = "https://api.spotify.com/v1/browse/new-releases"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)['albums']['items']
#     # return json_result
#     print(json_result)

def get_artist_shows(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/shows"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    # return json_result
    print(json_result)

# def player(token):
#     url = "https://api.spotify.com/v1/me/player"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)
#     print(json_result)

# token = get_token()
# result = get_artist_id(token, 'Tool')
# artist_id = result['id']
# songs = get_songs_by_artist(token, artist_id)

# player(token)
# get_artist_shows(token, artist_id)
# search_show(token, "Bad Bunny")


# get_new_releases(token, artist_id)

# related = related_artists(token, artist_id)
# for idx, artist in enumerate(related):
#     print(f"{idx + 1}. {artist['name']}")

# for idx, song in enumerate(songs):
#     print(f"{idx + 1}. {song['name']}")

# streamlit app title
st.title("Spotify App - Top 10 Tracks")

# text input
artist_name = st.text_input("Enter artist name: ")

if st.button("Search"):
    if artist_name:
        token = get_token()
        artist_info = get_artist_id(token, artist_name)
        artist_id = artist_info['id']
        
        if artist_info:
            
            # col1, col2, col3 = st.columns(3)
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            with col1:
                st.header(f"Top Tracks by {artist_name}")
                songs = get_songs_by_artist(token, artist_info['id'])
                for idx, song in enumerate(songs):
                    # st.write(f"{idx + 1}. {song['name']}")
                    st.write(f"{idx + 1}. [{song['name']}](https://open.spotify.com/track/{song['id']})")
            with col2:
                st.header(f"Artists related to {artist_name}")
                related = related_artists(token, artist_id)
                for idx, artist in enumerate(related):
                    if idx == 10:
                        break
                    # st.write(f"{idx + 1}. {artist['name']}")
                    st.write(f"{idx + 1}. [{artist['name']}](https://open.spotify.com/artist/{artist['id']})")
            # with col3:
                # st.header("Shows: ")
                # shows = get_artist_shows(token, artist_id)
                # for show in shows:
                #     st.write(f"{show['date']} - {show['venue']['name']}, {show['venue']['city']['name']}, {show['venue']['country']}")
                # st.header("Playback menu: ")
                # st.write("Click link to play on Spotify")
            with col3:
                st.header("Recommended Tracks")
            
            with col4:
                st.header("")
        else:
            st.write("No artist with this name exists...")
    else:
        st.write("Please enter an artist name.")
