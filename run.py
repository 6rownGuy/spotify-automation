# This script will take song names as inputs
# and create a spotify playlist using those songs.

from spotify_client import client_id, client_sectet, username, redirect_uri
import spotipy
from spotipy import SpotifyOAuth
import json

print('\n\n\n')

# Specifying the scope and access token for the spotify api

scope = 'playlist-modify-public'
token = SpotifyOAuth(client_id=client_id, client_secret=client_sectet,
                     redirect_uri=redirect_uri, scope=scope, username=username)
spotify_object = spotipy.Spotify(auth_manager=token)


# Asking user for playlist name and description
playlist_name = input('Enter a playlist name: ')
playlist_description = input('Enter a playlsit description: ')

spotify_object.user_playlist_create(
    user=username, name=playlist_name, public=True, description=playlist_description)

user_input = input('Enter a song: ')
tracks = []
seed_artists = []
seed_tracks = []


# The seed_tracks and seed_artists can hold a combined of 5
# values between themselves.
# The ctr variable is used to control the flow of values into
# those variables and to ensure that they get no more than
# 5 values combined.
ctr = 0

# Loop terminated when user enters 'done' in the console
while user_input != 'done':
    ctr += 1

    # Search for user_input
    result = spotify_object.search(q=user_input)
    
    # From search results, append track uri to tracks list
    tracks.append(result['tracks']['items'][0]['uri'])
    
    # First 2 track IDs are added into seed_tracks
    if(ctr <= 2):
        seed_artists.append(result['tracks']['items'][0]['artists'][0]['uri'])

    # Next 3 artist IDs are added into seed_artists    
    if(ctr > 2 and ctr <= 5):
        seed_tracks.append(result['tracks']['items'][0]['id'])

    user_input = input('Enter a song: ')

# Now we have to find the playlist we just created and add the songs to it

prePlaylist = spotify_object.user_playlists(user=username)

# Getting the playlist id from prePlaylist
playlist_id = prePlaylist['items'][0]['id']

# Adding tracks to the playlist
spotify_object.user_playlist_add_tracks(
    user=username, playlist_id=playlist_id, tracks=tracks)

print('Your brand new playlist has been created!')


# recommendation_info will hold the json
# returned from spotify_object.recommendations()
recommendation_info = spotify_object.recommendations(
    seed_artists=seed_artists, seed_tracks=seed_tracks,  limit=10)

# Empty list of recommended tracks
recommended_tracks = []

i = 0
while i < 10:
    # Appending the song names to recommended_tracks list
    recommended_tracks.append(recommendation_info['tracks'][i]['name'])
    i += 1

print('Here are some recommended tracks for you:')

for track in enumerate(recommended_tracks, 1):
    print(f"{track[0]}. {track[1]} ")