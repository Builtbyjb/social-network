# Generated by Django 5.0.6 on 2024-08-22 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='following_user_id',
        ),
        migrations.RemoveField(
            model_name='following',
            name='user_id',
        ),
    ]
