import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.template.defaultfilters import escape
from django.template.loader import render_to_string
from django.conf import settings


class ChatManager(models.Manager):
    def public(self):
        """Returns only public chats."""
        return self.get_query_set().filter(is_public=True)

class Chat(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    updated = models.DateTimeField(auto_now_add=True)
    
    # Use the custom manager defined above
    objects = ChatManager()
    
    class Meta:
        ordering = ('name', 'created')
        app_label = 'watercooler'
    
    def users(self):
        return User.objects.filter(posts__parent__pk=self.id).distinct()
    
    @models.permalink
    def get_absolute_url(self):
        return ('chat', [self.slug])
    
    def __unicode__(self):
        return u'%s' % self.name


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    parent = models.ForeignKey(Chat, related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    class Meta:
        ordering = ('timestamp',)
        get_latest_by = 'timestamp'
        order_with_respect_to = 'parent'
        app_label = 'watercooler'
        
    def __unicode__(self):
        return 'Post by %s on %s' % (self.user, self.parent)


def update_chat_on_post_save(sender, **kwargs):
    """When a Post object is created, set its parent Chat object's
    updated time to now."""
    created = kwargs['created']
    instance = kwargs['instance']
    if created:
        instance.parent.updated = datetime.datetime.now()
        instance.parent.save()

# Wire up the signal to listen for Post objects being saved
post_save.connect(update_chat_on_post_save, sender=Post)
