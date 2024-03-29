# spotify_integration/views.py
import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .models import SpotifyTracksRequest, UserProfile


def start(request):
    return render(request, "start.html")


def profile(request):
    return render(request, "profile.html")


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
        if response.status_code == 200:
            access_token = response.json()["access_token"]
            refresh_token = response.json()["refresh_token"]
            request.session["access_token"] = access_token
            request.session["refresh_token"] = refresh_token
            # Use access token to fetch recently played tracks
            recently_played_url = (
                "https://api.spotify.com/v1/me/player/recently-played?limit=50"
            )
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(recently_played_url, headers=headers)
            if response.status_code == 200:
                tracks_data = response.json()["items"]
                request.session["tracks_data"] = tracks_data
                print(f"hi {tracks_data}")

    # If user submits registration form
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile and save access token
            profile = UserProfile.objects.create(
                user=user, access_token=request.session.get("access_token")
            )
            # Save tracks associated with the newly created user
            tracks_data = request.session.get("tracks_data")
            if tracks_data:
                SpotifyTracksRequest.objects.create(
                    user=user,
                    tracks_data=tracks_data,
                    access_token=request.session.get("access_token"),
                )
            login(request, user)
            return redirect(
                "profile_page"
            )  # Redirect to track list page after registration
    else:
        form = UserCreationForm()

    return render(request, "redirect.html", {"form": form, "tracks_data": tracks_data})
