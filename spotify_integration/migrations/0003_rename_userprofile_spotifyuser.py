# Generated by Django 5.0.3 on 2024-04-14 19:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_integration', '0002_rename_track_data_spotifytracksrequest_tracks_data'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='SpotifyUser',
        ),
    ]