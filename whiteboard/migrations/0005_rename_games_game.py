# Generated by Django 3.2.14 on 2022-07-19 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whiteboard', '0004_games_banner'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Games',
            new_name='Game',
        ),
    ]
