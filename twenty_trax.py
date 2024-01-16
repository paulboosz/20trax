import json
import re
from PIL import Image
import requests
import pytesseract
import argparse
from io import BytesIO
import logging
from spotipy import Spotify
from spotipy.util import prompt_for_user_token

logging.basicConfig(level=logging.DEBUG)


def remove_leading_trailing_non_alphanumeric_and_whitespace(s):
    s = s.strip()
    s = re.sub(r"^[^\w]+|[^\w]+$", "", s)
    s = re.sub(r"^\d+[.,]? ", "", s)
    return s


def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)


def convert_to_list(s):
    return [
        remove_leading_trailing_non_alphanumeric_and_whitespace(line.strip())
        for line in s.split("\n")
        if line.strip() != ""
    ]


def image_to_text(image_url):
    response = requests.get(image_url)
    if response.status_code != 200:
        logging.error("Failed to fetch image.")
        return []
    img_data = BytesIO(response.content)
    img = Image.open(img_data)
    extracted_text = pytesseract.image_to_string(img)
    return convert_to_list(extracted_text)


def main(image_url, playlist_name, config):
    token = prompt_for_user_token(
        config["SPOTIFY_USERNAME"],
        "playlist-modify-private playlist-modify-public",
        config["SPOTIFY_CLIENT_ID"],
        config["SPOTIFY_CLIENT_SECRET"],
        config["SPOTIFY_REDIRECT_URI"],
    )

    if not token:
        logging.error("Failed to get token.")
        return

    sp = Spotify(auth=token)

    songs = image_to_text(image_url)
    if not songs:
        logging.error("No songs extracted from the image.")
        return

    print(f"OCR identified songs:")
    for song in songs:
        print(song)

    playlist = sp.user_playlist_create(config["SPOTIFY_USERNAME"], playlist_name)
    playlist_id = playlist["id"]

    track_uris = []
    for song in songs:
        if song:
            results = sp.search(q=song, type="track", limit=1)
            if not results["tracks"]["items"]:
                logging.warning(f"No track found for song: {song}")  
                continue          
            track_uris.append(results["tracks"]["items"][0]["uri"])
            logging.info(f"Found track: {song}")
        else:
            print("Song query is empty.")

        
    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)
        logging.info("Tracks added to playlist successfully!")
    else:
        logging.info("No tracks found to add to the playlist.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an image URL to extract song names and add them to a Spotify playlist.")
    parser.add_argument("image_url", type=str, help="URL of the image.")
    parser.add_argument("playlist_name", type=str, help="Name of the Spotify playlist to be created.")
    parser.add_argument("--config", type=str, default="config.json", help="Path to configuration file.")
    args = parser.parse_args()

    config = load_config(args.config)

    main(args.image_url, args.playlist_name, config)
