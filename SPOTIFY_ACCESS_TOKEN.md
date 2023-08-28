# How to get the SPOTIFY_ACCESS_TOKEN

1. Set Up Spotify Developer Account:
   If you don't have one, go to the Spotify Developer Dashboard and log in or sign up.
   Create a new App from the dashboard. This will give you a Client ID and Client Secret, which you'll use to authenticate your requests.

2. Authorization Code Flow:
   Redirect the user to the Spotify Accounts service's authorization endpoint:

`https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=playlist-modify-public`
Replace {CLIENT_ID} with your Client ID and {REDIRECT_URI} with a valid redirect URI you've set in your Spotify Developer Dashboard for your app. The scope playlist-modify-public is necessary to create public playlists.

After the user authorizes, they'll be redirected to your specified redirect URI with a code in the query string. Capture this code.

Exchange this code for an access token by making a POST request:

`curl -H "Authorization: Basic {BASE64_ENCODED_CLIENT_ID_AND_SECRET}" -d grant_type=authorization_code -d code={CODE} -d redirect_uri={REDIRECT_URI} https://accounts.spotify.com/api/token`

Replace {BASE64_ENCODED_CLIENT_ID_AND_SECRET} with the base64 encoded string of your client_id:client_secret, {CODE} with the code you received in the previous step, and {REDIRECT_URI} with your redirect URI.

This will return an access token and a refresh token. Use this access token in your script.
