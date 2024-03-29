# spotify_integration/views.py
import requests
from django.conf import settings
from django.shortcuts import redirect, render


def start(request):
    return render(request, "start.html")


def authorize_spotify(request):
    # Redirect the user to Spotify's authorization page
    spotify_auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": "user-read-recently-played",
    }
    auth_url = f"{spotify_auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return redirect(auth_url)


def spotify_redirect(request):
    # Handle callback after user authorizes with Spotify
    code = request.GET.get("code")
    tracks_data = []
    if code:
        # Exchange code for access token
        token_url = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        }
        response = requests.post(token_url, data=data)
        print(f"hi {response.json()}")
        if response.status_code == 200:
            access_token = response.json()["access_token"]
            # Use access token to fetch recently played tracks
            recently_played_url = (
                "https://api.spotify.com/v1/me/player/recently-played?limit=50"
            )
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(recently_played_url, headers=headers)
            if response.status_code == 200:
                tracks_data = response.json()["items"]
                print(f"hi {tracks_data}")
                # for track_data in tracks_data:
                #     # Save recently played tracks to the database
                #     Track.objects.create(
                #         name=track_data['track']['name'],
                #         artist=track_data['track']['artists'][0]['name'],
                #         # Add more fields as needed
                #     )
    return render(request, "redirect.html", {"tracks_data": tracks_data})
