from django.core.management.base import BaseCommand

from spotify_integration.models import SpotifyUser


class Command(BaseCommand):
    help = "Get new data from the Spotify API and process them to plays"

    def handle(self, *args, **kwargs):
        for user in SpotifyUser.objects.all():
            user.get_refresh_token()
            result = user.get_recently_played()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully retrieved tracks for "%s"' % result.user
                )
            )
            if result:
                result.create_spotify_plays()
