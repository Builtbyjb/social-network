# Generated by Django 5.0.6 on 2024-09-03 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_remove_following_following_user_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Liked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]
