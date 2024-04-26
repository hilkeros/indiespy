from django.contrib import admin

from .models import SpotifyTracksRequest


class SpotifyTracksRequestAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "access_token",
    ]


# Register your model with the admin site
admin.site.register(SpotifyTracksRequest, SpotifyTracksRequestAdmin)
