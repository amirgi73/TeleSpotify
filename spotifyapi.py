import sys
import spotipy
import spotipy.util as util
import os
from youtube import download_mp3, logger
import eyed3
import requests

scope = 'user-library-read playlist-read-private'
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REDIRECT_URL = os.environ.get('SPOTIFY_REDIRECT_URL')

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print(f"Usage: {sys.argv[0]} username")
    sys.exit()

token = util.prompt_for_user_token(
    username, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)
tracks = []
if token:
    spo = spotipy.Spotify(auth=token)
    # the user_playlist_tracks function gets two parametrs: 'user' and 'playlist'
    # which can be extracted from the playlist uri
    results = spo.user_playlist_tracks(
        'bnotmjg1ue4zu2d06ovib5sd6', '4ybqmPofUM18af8BtinhV9')

    for item in results['items']:
        cover = item['track']['album']['images'][0]['url']
        track_name = item['track']['name']
        track_artists = []
        for artist in item['track']['artists']:
            track_artists.append(artist['name'])
        track_album = item['track']['album']['name']
        tracks.append({'name': track_name, 'artists': track_artists,
                       'album': track_album, 'cover_url': cover})
else:
    print(f"can't get token for {username}")
    logger.error(f"can't get token for {username}")

if __name__ == "__main__":
    for track in tracks:
        title = track['name']
        artists = track['artists']
        album = track['album']
        file_name = f'Downloads/{title} - {album}.mp3'
        if not os.path.isfile(file_name):
            download_mp3(f"{title} {artists[0]}", title, album)
            with open('cover.jpg', 'wb') as cover:
                cover.write(requests.get(track['cover_url']).content)
            try:
                audiofile = eyed3.load(file_name)
                audiofile.tag.title = title
                audiofile.tag.artist = f"{','.join(artists)}"
                audiofile.tag.album = album
                audiofile.tag.images.set(
                    3, open('cover.jpg', 'rb').read(), 'image/jpeg')
                audiofile.tag.save()
            except OSError as e:
                logger.error(f"Couldn't set mp3 tags: {e}")
            try:
                os.remove('cover.jpg')
            except OSError:
                pass
        else:
            logger.debug(f'file exists, Skipping {file_name} ...')
