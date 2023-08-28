# Spotify Playlist Creator from Image

A script that processes an image URL to extract song names and add them to a Spotify playlist.

[The tweet that started this](https://twitter.com/heathensquirrel/status/1693203564703653956)

![](https://imgur.com/a/HdOxpKi)
![](https://imgur.com/KOIEKhB)

## Description

This script uses Optical Character Recognition (OCR) to extract song names from an image. After extracting the song names, it interfaces with the Spotify API to search for these songs and add them to a specified playlist.

## Prerequisites

- Python 3.x
- A Spotify Developer account and a registered App to get the necessary API token.

## Installation

1. Clone the repository:
   git clone <repository_url>

css
Copy code

2. Navigate to the project directory:
   cd <repository_directory_name>

markdown
Copy code

3. Install the required libraries:
   pip install -r requirements.txt

markdown
Copy code

4. Update the `config.json` with your Spotify API token and user ID.

## Usage

python script_name.py <image_url> "<playlist_name>"

markdown
Copy code

- `image_url`: The URL of the image containing the list of songs.
- `playlist_name`: The name of the Spotify playlist to be created or updated.

For example:
python script_name.py https://example.com/path/to/image.png "My Awesome Playlist"

python
Copy code

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
Now, you can copy the content above and paste it into a text editor to save it as README.md
