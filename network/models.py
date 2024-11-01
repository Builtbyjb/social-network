from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)

class Posts(models.Model):
    username = models.CharField(max_length=100)
    user_id = models.IntegerField()
    post = models.CharField(max_length=500)
    timestamp = models.DateTimeField()
    likes = models.IntegerField(default=0)

class Following(models.Model):
    username = models.CharField(max_length=100)
    following_username = models.CharField(max_length=100) 

class Liked(models.Model):
    post_id = models.IntegerField()
    username = models.CharField(max_length=100)