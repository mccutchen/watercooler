from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    chat = models.ForeignKey(Chat)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
