import requests
from PIL import Image
import json
import pytesseract
import argparse
from io import BytesIO
import logging
import re

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)


def remove_leading_trailing_non_alphanumeric_and_whitespace(s):
    # First, strip the string to remove leading and trailing whitespaces
    s = s.strip()
    # Then, use regular expression to remove leading and trailing non-alphanumeric characters
    s = re.sub(r"^[^\w]+|[^\w]+$", "", s)
    s = re.sub(r"^\d+[.,]? ", "", s)
    return s


def load_config(path="config.json"):
    """Load configuration from a JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def convert_to_list(s):
    """Convert block of text into a list of strings, separated by double newlines."""
    return [
        remove_leading_trailing_non_alphanumeric_and_whitespace(line.strip())
        for line in s.split("\n")
        if line.strip() != ""
    ]


def image_to_text(image_url):
    """Extract text from an image given its URL."""
    response = requests.get(image_url)
    if response.status_code != 200:
        logging.error("Failed to fetch image.")
        return []

    img_data = BytesIO(response.content)
    img = Image.open(img_data)
    extracted_text = pytesseract.image_to_string(img)
    return convert_to_list(extracted_text)


def create_playlist(playlist_name, user_id, headers):
    """Create a new Spotify playlist."""
    response = requests.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        headers=headers,
        json={
            "name": playlist_name,
            "description": "made with https://github.com/paulboosz/20trax",
            "public": True,
        },
    )
    if response.status_code != 201:
        logging.error("Failed to create playlist.")
        return None
    return response.json()["id"]


def main(image_url, playlist_name, config):
    songs = image_to_text(image_url)
    if not songs:
        logging.error("No songs extracted from the image.")
        return
    print(f"OCR identified songs :")
    for song in songs:
        print(song)

    playlist_id = create_playlist(
        playlist_name,
        config["SPOTIFY_USER_ID"],
        headers,
    )
    if not playlist_id:
        return

    # Add tracks to the playlist
    track_uris = []
    for song in songs:
        search_response = requests.get(
            f"https://api.spotify.com/v1/search?q={song}&type=track&limit=1",
            headers=headers,
        )
        if search_response.status_code != 200:
            logging.warning(f"Failed to find track for song: {song}")
            continue
        tracks = search_response.json()["tracks"]["items"]
        if not tracks:
            logging.warning(f"No track found for song: {song}")
            continue
        track_uris.append(tracks[0]["uri"])

    if track_uris:
        add_tracks_response = requests.post(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            headers=headers,
            json={"uris": track_uris},
        )
        if add_tracks_response.status_code != 201:
            logging.error("Failed to add tracks to playlist.")
        else:
            logging.info("Tracks added to playlist successfully!")
    else:
        logging.info("No tracks found to add to the playlist.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process an image URL to extract song names and add them to a Spotify playlist."
    )
    parser.add_argument("image_url", type=str, help="URL of the image.")
    parser.add_argument(
        "playlist_name", type=str, help="Name of the Spotify playlist to be created."
    )
    parser.add_argument(
        "--config", type=str, default="config.json", help="Path to configuration file."
    )
    args = parser.parse_args()

    config = load_config(args.config)
    headers = {
        "Authorization": f"Bearer {config['SPOTIFY_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    }

    main(args.image_url, args.playlist_name, config)
