from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
import os
import logging
from logger import Logger
import spotifyapi
import telegram

logging.basicConfig(format="%(asctime)s - %(name)s\t%(levelname)s:\t%(message)s", level=logging.INFO)
logger = Logger('bot')

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
updater = Updater(token=TELEGRAM_TOKEN, request_kwargs={'read_timeout': 100, 'connect_timeout': 10})
dispatcher = updater.dispatcher
job_q = dispatcher.job_queue
sent_tracks = {}


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


button_list = [
    telegram.InlineKeyboardButton("Check Spotify", callback_data='CheckSpotify'),
]
reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=f"Just Testing...Nothing funny here."
    "get out")


def send_music(file_to_send, bot, update):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    audio = open(file_to_send, 'rb')
    bot.send_audio(chat_id=chat_id, audio=audio, timeout=300, caption=f'Send by @{username}')


def is_new_member(bot, update):
    for member in update.message.new_chat_members:
        if member.username == "TeleSpotifyBot":
            bot.sendMessage(chat_id=update.message.chat_id, text="Hello Guys! I'll send You awsome musics")


def get_tracks(bot, update):
    chat_id = update.message.chat_id
    tracks = os.listdir('Downloads/')
    if chat_id not in sent_tracks.keys():
        sent_tracks[chat_id] = []
    for track in tracks:
        logger.debug(f"sent_tracks={sent_tracks}")
        if track not in sent_tracks.get(chat_id, []):
            send_music(os.path.join('Downloads', track), bot, update)
            sent_tracks[chat_id].append(track)


def start_sending_tracks(bot, update):
    get_tracks(bot, update)


def check_spotify(bot, update=None, **kwargs):
    if update:
        username = update.message.from_user.username
        chat_id = update.message.chat_id
    else:
        print(**kwargs['chat_data'])
    bot.send_message(chat_id=chat_id, text=f'Checking Spotify for @{username}')
    spotifyapi.main()
    start_sending_tracks(bot, update)


# Handlers:
group_handler = MessageHandler(Filters.status_update.new_chat_members, is_new_member)
start_handler = CommandHandler('start', callback=start)
spotify_handler = CommandHandler('CheckSpotify', check_spotify)

# adding Handlers to dispatcher
dispatcher.add_handler(group_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(spotify_handler)
# dispatcher.add_handler(CallbackQueryHandler(check_spotify, pass_chat_data=True,
#                                             pattern=r'CheckSpotify'))
# music_job = job_q.run_repeating(start_sending_tracks, interval=300, first=0)
updater.start_polling()
