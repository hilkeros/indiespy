from django.core.management.base import BaseCommand, CommandError

from spotify_integration.models import SpotifyUser


class Command(BaseCommand):
    help = "Get new data from the Spotify API and process them to plays"

    def handle(self, *args, **kwargs):
        for user in SpotifyUser.objects.all():
            try:
                user.get_refresh_token()
                result = user.get_recently_played()
                if result:
                    result.create_spotify_plays()
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Successfully retrieved tracks for "%s"' % result.user
                        )
                    )
            except result.user.DoesNotExist:
                raise CommandError('Couldnt fetch data for Spotify User "%s"' % user)
