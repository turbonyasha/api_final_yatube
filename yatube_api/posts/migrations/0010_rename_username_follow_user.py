# Generated by Django 3.2.16 on 2024-09-18 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_rename_user_follow_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='username',
            new_name='user',
        ),
    ]
