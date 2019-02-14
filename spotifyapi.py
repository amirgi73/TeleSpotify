import sys
import spotipy
import spotipy.util as util
import os
from logger import Logger
from youtube import download_mp3
import eyed3
import requests

logger = Logger('spotifyapi')
if len(sys.argv) > 2:
    username = sys.argv[1]
else:
    print(f"Usage: {sys.argv[0]} username playlist-uri")
    sys.exit()


def playlist_uri_parser(uri):
    try:
        u = uri.split(':')[2]
        p = uri.split(':')[4]
    except IndexError as e:
        logger.error(f"Invalid URI... {e}")
        print('Invalid URI...')
        sys.exit()
    return u, p


scope = 'user-library-read playlist-read-private'
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REDIRECT_URL = os.environ.get('SPOTIFY_REDIRECT_URL')
SPOTIFY_PLAYLIST_USER, SPOTIFY_PLAYLIST = playlist_uri_parser(sys.argv[2])

playlist_user, playlist = playlist_uri_parser(sys.argv[2])
token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)
tracks = []
if token:
    spo = spotipy.Spotify(auth=token)
    results = spo.user_playlist_tracks(SPOTIFY_PLAYLIST_USER, SPOTIFY_PLAYLIST)

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
                audiofile.tag.images.set(3, open('cover.jpg', 'rb').read(), 'image/jpeg')
                audiofile.tag.save()
            except OSError as e:
                logger.error(f"Couldn't set mp3 tags: {e}")
            try:
                os.remove('cover.jpg')
            except OSError:
                pass
        else:
            logger.debug(f'File exists, Skipping {file_name} ...')
