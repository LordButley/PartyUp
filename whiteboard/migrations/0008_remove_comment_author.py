# Generated by Django 3.2.14 on 2022-07-22 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whiteboard', '0007_comment_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
    ]
