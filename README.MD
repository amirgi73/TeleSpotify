# TeleSpotify

TeleSpotify is a project aiming to create a Telegram bot which parses the spotify urls and downloads the mp3 files. **So you can share your music with others who don't have spotify.**


# Requirements

 - `python3`
 - `pipenv`
 - `spotipy`
 - `requests`
 - `youtube-dl`
 - `ffmpeg`
 - `python-magic-bin`
 - `google-api-python-client`
 - `eyed3`
 - spotify developer api  
 - youtube developer api

## Install requirements

First install python3 for your OS.
Then install pipenv using:

    pip3 install pipenv --user
Clone the repository using git:

    git clone https://github.com/amirgi73/TeleSpotify.git

Now you can install all dependencies using pipenv:

    pipenv install

## Making the necessary changes:
Set the necessary environment variables:

    export SPOTIFY_CLIENT_ID='your-client-id'
    export SPOTIFY_CLIENT_SECRET='your-client-secret'
    export SPOTIFY_REDIRECT_URL='spotify-app-redirect-url'
    export YOUTUBE_API_SECRET='your-youtube-api'

Open `spotifyapi.py` in your text editor and find the following line:

    results = spo.user_playlist_tracks('bnotmjg1ue4zu2d06ovib5sd6', '4ybqmPofUM18af8BtinhV9')
**Replace** the parameters of function with your desired playlist specs. the first parameter is `user` and the second one is `playlist` which both can be extracted from your **playlist's URI**

## Run the Script

Now you can run the `spotifyapi.py` file which downloads your playlist tracks and saves them to the `Downloads` directory. Replace the `spotify-user-name` with **username** of the account which you want to download the playlist from:

    python3 spotifyapi.py spotify-user-name
The script will run and opens a browser window. Here you should log in to our spotify account and give the permission to the app so it can read your playlist. After granting the permission, your browser shows an error saying *the page you requested was not found*. **Please note that this is an expected behavior.** 
 **copy the url** of the page which is showing you the error and paste it in your terminal where the script prompts it.

## Setting log level

You can set the log level in the `youtube.py` file. Please read the comment block in `youtube.py` to understand what each level means. The logs will be saved in the `youtube.log` file.

## to_do:

 1. developing telegram integration
 2. completing the logging functionality
 3. monitor the desired playlist to catch added tracks ASAP
 4. ...