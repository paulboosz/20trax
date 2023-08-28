# Spotify Playlist Creator from Image

A script that processes an image URL to extract song names and add them to a Spotify playlist.

[The tweet that started this](https://twitter.com/heathensquirrel/status/1693203564703653956)

![tweet](https://imgur.com/a/HdOxpKi)
![first_image](https://imgur.com/KOIEKhB)

## Description

This script uses Optical Character Recognition (OCR) to extract song names from an image. After extracting the song names, it interfaces with the Spotify API to search for these songs and add them to a specified playlist.

## Prerequisites

- Python 3.x
- A Spotify Developer account and a registered App to get the necessary API token.

Update the `config.json` with your Spotify API token and user ID.

## Usage

```$ python script_name.py <image_url> "<playlist_name>"```


- `image_url`: The URL of the image containing the list of songs.
- `playlist_name`: The name of the Spotify playlist to be created or updated.

For example:
```python script_name.py https://example.com/path/to/image.png "Nick's 20trax"```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
