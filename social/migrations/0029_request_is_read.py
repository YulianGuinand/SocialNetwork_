# Generated by Django 5.0.3 on 2024-03-05 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0028_rename_studient_meeting_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
