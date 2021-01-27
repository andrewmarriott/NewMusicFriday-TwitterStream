"""SPOTIFY API ACCESS KEY"""

from creds import *
client_id = c_client_id
client_secret = c_client_secret


import base64
from urllib.parse import urlencode
import requests


def get_client_creds():
	client_creds = f"{client_id}:{client_secret}"
	client_creds_b64 = base64.b64encode(client_creds.encode())
	return client_creds_b64.decode()


def authentication():
	client_creds_b64 = get_client_creds()
	token_url = "https://accounts.spotify.com/api/token"
	token_data = {
			"grant_type": "client_credentials" 
		}
	token_headers = { 
			"Authorization": f"Basic {client_creds_b64}"
		}
	r = requests.post(token_url, data=token_data, headers=token_headers)
	data = r.json()
	access_token = data['access_token']
	return access_token


count = 0
artist_list = []
#grab the top tracks from the playlist
def get_playlist_data(playlist_uri):
	#setting up the headers and parameters for the API request
	access_token = authentication()
	headers = {
			"Authorization": f"Bearer {access_token}" 
        }
	playlist_id = playlist_uri[17:]
	endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"
	params = urlencode({"market":"US", "limit": "1"})
	#run the API request
	lookup_url = f"{endpoint}?{params}"
	r = requests.get(lookup_url, headers=headers)
	playlist_data = r.json()
	#stop after grabbing the first track and return the name
	for track in playlist_data['tracks']['items']:
		artist_list.append((track['track']['artists'][0]['name']))
	return artist_list


