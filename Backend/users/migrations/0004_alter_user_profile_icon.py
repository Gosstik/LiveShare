# Generated by Django 5.2 on 2025-04-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_profile_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_icon',
            field=models.ImageField(blank=True, null=True, upload_to='profile_icons'),
        ),
    ]
