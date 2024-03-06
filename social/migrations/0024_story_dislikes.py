# Generated by Django 5.0.2 on 2024-02-25 16:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0023_story_is_follow'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='dislikesstory', to=settings.AUTH_USER_MODEL),
        ),
    ]