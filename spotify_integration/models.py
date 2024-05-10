import ast
from datetime import datetime

import requests
from django.conf import settings
from django.db import models

from users.models import CustomUser


class SpotifyUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)

    def get_recently_played(self):
        recently_played_url = (
            "https://api.spotify.com/v1/me/player/recently-played?limit=50"
        )
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(recently_played_url, headers=headers)
        if response.status_code == 200:
            tracks_data = response.json()["items"]
            if tracks_data:
                SpotifyTracksRequest.objects.create(
                    user=self.user,
                    tracks_data=tracks_data,
                    access_token=self.access_token,
                )
                print("New tracks data saved")

    def get_refresh_token(self):
        refresh_token_url = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        }
        response = requests.post(refresh_token_url, data=data)
        if response.status_code == 200:
            access_token = response.json()["access_token"]
            # refresh_token = response.json()["refresh_token"]
            self.access_token = access_token
            # self.refresh_token = refresh_token
            self.save()
            print("Tokens refreshed")


class SpotifyTracksRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    tracks_data = models.TextField()

    def create_spotify_plays(self):
        request_dict = ast.literal_eval(self.tracks_data)
        for track in request_dict:
            timestamp_str = track["played_at"]
            timestamp = datetime.fromisoformat(timestamp_str[:-1])
            SpotifyPlay.objects.create(
                user=self.user,
                played_at=timestamp,
                track_id=track["track"]["id"],
                name=track["track"]["name"],
                artist_id=track["track"]["artists"][0]["id"],
                artist_name=track["track"]["artists"][0]["name"],
                popularity=track["track"]["popularity"],
            )


class SpotifyPlay(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    played_at = models.DateTimeField()
    track_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    artist_id = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    popularity = models.IntegerField()
