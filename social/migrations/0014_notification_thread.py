# Generated by Django 5.0.2 on 2024-02-22 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0013_threadmodel_messagemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='social.threadmodel'),
        ),
    ]
