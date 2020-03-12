from tkinter import *
import youtube_to_spotify as ys


window = Tk()
window.title("Youtube to Spotify")
window.configure(background="black")

Label(window, text="Enter the Youtube Playlist URL", background="black", fg="white") .grid(row=0, column=1, sticky=W)

playlistUrlText = Entry(window, fg="grey")
playlistUrlText.grid(row=1, column=1, columnspan=3)


def create_playlist():
    playlistUrl = playlistUrlText.get()
    playlistId = ys.get_playlist_id(playlistUrl)
    spotify = ys.get_user_info()
    allSongs = ys.get_all_songs(spotify, playlistId)
    spotifyPlaylistId = ys.create_playlist(spotify)
    ys.fill_playlist(spotify, allSongs, spotifyPlaylistId)


playlistUrlButton = Button(window, text="SUBMIT", width="6", command=create_playlist)
playlistUrlButton.grid(row=2, column=1, columnspan=1)

window.mainloop()
