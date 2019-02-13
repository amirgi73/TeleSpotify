import logging
import os
import youtube_dl
from googleapiclient.discovery import build

LOGGING_OPTS = {
    0: logging.ERROR,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG
}
# sets the logging level:
#   0:  only errors will be logged
#   1:  errors and warnings will be logged. This is the default behavior
#   3:  errors, warnings and info messages will be logged
#   4:  debug messages will be logged too.
logging_level = 3

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_OPTS.get(logging_level))
fh = logging.FileHandler(f'{__name__}.log')
formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s:\t %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VIDEO = 'youtube#video'
YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v='
VERSION = '3.0.1'
YOUTUBE_API_SECRET = os.environ.get('YOUTUBE_DEV_KEY')


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
    print(f"Trying to Download the '{title}' from '{album}' album")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([get_youtube_url(search_term)])
    except:
        print(f"failed to download {title}...")
        logger.error(f"failed to download {title}...")
