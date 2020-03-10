import requests
import os
import youtube_dl
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

import google.oauth2.credentials
from googleapiclient.discovery import build

#get playlist url

def get_playlist_id():
    print("Enter playlist url:")
    playlist_url = input()
    temp = playlist_url.split('list=')
    playlist_id = temp[1]
    return(playlist_id)

#get all songs
def get_all_songs():
    all_songs = {}
    api_key = "AIzaSyC-EFzT3sBTA6oIjtHFFWkZmXdMyVaoxlo"

    youtube = build('youtube', 'v3', developerKey=api_key)

    playlist_id = get_playlist_id()

    playlist = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
        ).execute()

    all_songs = []
    for video in playlist['items']:
        vid_title = video['snippet']['title']
        vid_url = "https://www.youtube.com/watch?v={}".format(video["snippet"]["resourceId"]["videoId"])
        song = youtube_dl.YoutubeDL({}).extract_info(vid_url, download=False)
        song_name = song['track']
        song_artist = song['artist']
        if song_name is not None and song_artist is not None:
            all_songs.append(get_song_uri(song_name, song_artist))
    return all_songs

#get user info

def get_user_info():
    CLIENT_ID = '44029faf1e334935801075b140b8a8ea'
    CLIENT_SECRET = '6cd1d0d64c53443f8bfab97937439ba2'
    REDIRECT_URI = 'https://google.com'

    username = ''
    scope = 'playlist-modify-public user-read-private'

    token = util.prompt_for_user_token(username, scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    if token:
        spotify = spotipy.Spotify(auth=token)
    else:
        print("Couldn't get token")

    return spotify


spotify = get_user_info()
userId = spotify.current_user()['id']


#collect data from these songs
def get_song_uri(song_name, song_artist):
    query = song_name + ' - ' + song_artist
    song = spotify.search(q=query, limit=1, offset=0, type='track')['tracks']
    if len(song['items']) != 0:
        return song['items'][0]['uri']
    else:
        return '0'


#create playlist
def create_playlist():
    newPlaylist = spotify.user_playlist_create(user=userId,
    name='Youtube Playlist',
    public=True,
    description='Created from a Youtube Playlist')
    return newPlaylist['id']



#fill the playlist
def fill_playlist():

    uris = []
    for item in get_all_songs():
        uris.append(item)

    spotify.user_playlist_add_tracks(userId, create_playlist(), uris)


fill_playlist()
