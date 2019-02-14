from logger import Logger
import os
import youtube_dl
from googleapiclient.discovery import build

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VIDEO = 'youtube#video'
YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v='
VERSION = '3.0.1'
YOUTUBE_API_SECRET = os.environ.get('YOUTUBE_DEV_KEY')

logger = Logger('youtube')


class YdlLogger(object):
    def info(self, msg):
        pass

    def debug(self, msg):
        pass

    def warning(self, msg):
        logger.warning(msg)

    def error(self, msg):
        logger.error(msg)


def get_youtube_url(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_SECRET)
    search_response = youtube.search().list(q=query, part='id, snippet').execute()
    for item in search_response['items']:
        if item['id']['kind'] == 'youtube#video':
            return YOUTUBE_VIDEO_URL + item['id']['videoId']


def progreess_hook(d):
    if d['status'] == 'finished':
        logger.info(f'Done downloading: {d} now Converting...')
        print('--->\t[Done]')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': YdlLogger(),
    'progress_hooks': [progreess_hook],
}


def download_mp3(search_term, title, album):
    ydl_opts_ext = ydl_opts
    ydl_opts_ext['outtmpl'] = f"Downloads/{title} - {album}.%(ext)s"
    print(f"Trying to Download '{title}' from '{album}' album...", end='\t')
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([get_youtube_url(search_term)])
    except:
        print(f"failed to download {title}...")
        logger.error(f"failed to download {title}...")
