from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    
    class Meta:
        ordering = ('created',)
    
    def __unicode__(self):
        return u'%s' % self.name


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    parent = models.ForeignKey(Chat, related_name='posts'))
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    content_rendered = models.TextField()
    
    class Meta:
        ordering = ('timestamp',)
        get_latest_by = 'timestamp'
        order_with_respect_to = 'parent'
    
    def save():
        self.content_rendered = self.content
        super(Post, self).save()