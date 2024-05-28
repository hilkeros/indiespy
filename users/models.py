from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_spotify_play_count(self):
        return self.spotify_plays.count()

    def get_artists_overview(self):
        grouped_artists = self.spotify_plays.values(
            "artist_id", "artist_name"
        ).annotate(play_count=Count("artist_id"))
        sorted_by_popularity = grouped_artists.order_by("-play_count")
        return sorted_by_popularity
