# Generated by Django 5.0.2 on 2024-02-25 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0022_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='is_follow',
            field=models.BooleanField(default=False),
        ),
    ]
