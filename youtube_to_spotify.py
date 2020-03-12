import requests
import os
import youtube_dl
import spotipy
import spotipy.util as util
from googleapiclient.discovery import build


def get_playlist_id(playlistUrl):
    # ask user for url of the playlist and returns the id of the playlist
    playlistId = playlistUrl.split('list=')[1]
    return(playlistId)


# get all songs
def get_all_songs(spotify, playlistId):
    # precreated youtube api key
    apiKey = "AIzaSyC-EFzT3sBTA6oIjtHFFWkZmXdMyVaoxlo"
    youtube = build('youtube', 'v3', developerKey=apiKey)

    # gets the list of videos as playlistitem object from youtube api
    playlist = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlistId,
        maxResults=50
    ).execute()

    # extracts the name of song and artist from each video in playlist using youtube-dl library
    allSongs = []
    for video in playlist['items']:
        videoUrl = "https://www.youtube.com/watch?v={}".format(
            video["snippet"]["resourceId"]["videoId"])
        song = youtube_dl.YoutubeDL({}).extract_info(videoUrl, download=False)
        songName = song['track']
        songArtist = song['artist']
        if songName is not None and songArtist is not None:
            allSongs.append(get_song_uri(spotify, songName, songArtist))
    return allSongs


# get user info
def get_user_info():
    # spotify api secrets
    CLIENT_ID = '44029faf1e334935801075b140b8a8ea'
    CLIENT_SECRET = '6cd1d0d64c53443f8bfab97937439ba2'
    REDIRECT_URI = 'https://google.com'

    username = ''
    scope = 'playlist-modify-public user-read-private'

    # redirects to spotify authentication site to get the auth token of user
    token = util.prompt_for_user_token(
        username, scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    if token:
        spotify = spotipy.Spotify(auth=token)
    else:
        print("Couldn't get token")
    return spotify


# creates the spotify object from the user auth token


# returns the spotify uri of the given song and artist using spotify web api
def get_song_uri(spotify, songName, songArtist):
    query = songName + ' - ' + songArtist
    song = spotify.search(q=query, limit=1, offset=0, type='track')['tracks']
    if len(song['items']) != 0:
        return song['items'][0]['uri']
    else:
        return '0'


# creates an empty playlist using spotify web api
def create_playlist(spotify):
    userId = spotify.me()["id"]
    newPlaylist = spotify.user_playlist_create(user=userId,
                                               name='Youtube Playlist',
                                               public=True,
                                               description='Created from a Youtube Playlist')
    return newPlaylist['id']


# fills the playlist using spotify web api
def fill_playlist(spotify, allSongs, playlistId):
    userId = spotify.me()["id"]
    uris = []
    for item in allSongs:
        uris.append(item)

    spotify.user_playlist_add_tracks(userId, playlistId, uris)
