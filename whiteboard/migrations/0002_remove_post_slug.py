# Generated by Django 3.2.14 on 2022-07-13 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whiteboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]
