# Generated by Django 5.0.2 on 2024-02-21 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='user_has_seen',
            field=models.BooleanField(default=False),
        ),
    ]