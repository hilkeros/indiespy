from django.contrib import admin

from .models import SpotifyPlay, SpotifyTracksRequest


class SpotifyTracksRequestAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "access_token",
        "created_at",
    ]


admin.site.register(SpotifyTracksRequest, SpotifyTracksRequestAdmin)


class SpotifyPlayAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "played_at",
        "name",
        "artist_name",
        "track_id",
        "artist_id",
        "popularity",
        "created_at",
    ]


admin.site.register(SpotifyPlay, SpotifyPlayAdmin)
