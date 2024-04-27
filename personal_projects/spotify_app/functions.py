import requests
from requests import post, get
from dotenv import load_dotenv
import os
import base64
import json
import streamlit as st
import string
import base64
import hashlib
import secrets

# INIT
# def exchange_code_for_token(code, redirect_uri, client_id, client_secret):
#     url = "https://accounts.spotify.com/api/token"
#     data = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": redirect_uri,
#         "client_id": client_id,
#         "client_secret": client_secret
#     }
#     response = requests.post(url, data=data)
#     return response.json()

def load_env():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    return client_id, client_secret

def get_token(client_id, client_secret):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":"Basic " + auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }

    # data = {
    # 'grant_type': 'client_credentials',
    # 'client_id': client_id,
    # 'client_secret': client_secret,

    # }

    data = {
        "grant_type":"client_credentials",
        "Scope": "user-library-read user-read-private user-read-email"
        # 'scope':'user-read-private user-read-email user-library-read'
        }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']

    if token:
        print("Token obtained successfully:")
        print(token)
        print("Token Scopes:")
        print(json_result.get('scope'))
    else:
        print("Failed to obtain token. Response:")
        print(json_result)
        print("")   
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

# GET
def get_artist_id(token, artist_name):
    json_result = search_for_artist(token, artist_name)['artists']['items']
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result[0]

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

def get_artist_shows(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/shows"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    # return json_result
    print(json_result)

def get_user_saved_tracks(token, user_id=None, headers=None):
    url = f"https://api.spotify.com/v1/me/tracks"
    if headers != None:
        headers = headers 
    else:  
        headers = get_auth_header(token)
    response = get(url, headers=headers)
    json_result = json.loads(response.content)
    # print(headers)
    # print(response)
    return json_result

def generate_code_verifier():
    return secrets.token_urlsafe(100)

def generate_code_challenge(code_verifier):
    sha256_code_verifier = hashlib.sha256(code_verifier.encode()).digest()
    base64_url_encoded_code_challenge = base64.urlsafe_b64encode(sha256_code_verifier).decode().rstrip("=")
    return base64_url_encoded_code_challenge

def exchange_code_for_token(code, code_verifier, client_id, client_secret, redirect_uri):
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        'client_secret':client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier
    }
    response = requests.post(token_url, headers=headers, data=data)
    return response.json()