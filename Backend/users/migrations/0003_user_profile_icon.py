# Generated by Django 5.2 on 2025-04-26 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_friendinvitation_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_icon',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile_icons'),
        ),
    ]
