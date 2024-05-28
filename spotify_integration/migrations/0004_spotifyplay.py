# Generated by Django 5.0.3 on 2024-04-26 18:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_integration', '0003_rename_userprofile_spotifyuser'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyPlay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played_at', models.DateTimeField()),
                ('track_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('artist_id', models.CharField(max_length=255)),
                ('artist_name', models.CharField(max_length=255)),
                ('popularity', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]