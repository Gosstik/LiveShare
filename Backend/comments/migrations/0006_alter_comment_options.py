# Generated by Django 5.2 on 2025-04-14 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_alter_comment_created_at_alter_comment_edited_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Comments'},
        ),
    ]
