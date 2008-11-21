import datetime, time

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
        """Returns a dictionary containing a list of active user and
        a list of inactive users who have contributed to this chat."""
        # A user is inactive if they have not pinged in 20 seconds
        cutoff = datetime.datetime.now() - datetime.timedelta(0, 20)
        allusers = User.objects.filter(posts__parent__pk=self.id).distinct()
        active = [user for user in allusers if user.last_login > cutoff]
        inactive = [user for user in allusers if user.last_login < cutoff]
        return dict(active=active, inactive=inactive)
    
    @models.permalink
    def get_absolute_url(self):
        return ('chat', [self.slug])
    
    def __unicode__(self):
        return u'%s' % self.name


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    parent = models.ForeignKey(Chat, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    class Meta:
        ordering = ('created',)
        get_latest_by = 'created'
        order_with_respect_to = 'parent'
        app_label = 'watercooler'
    
    def timestamp(self):
        return int(time.mktime(self.created.timetuple()))
    
    def __unicode__(self):
        return 'Post by %s on %s' % (self.user, self.parent)


# ===================================================================
# Signal-handling functions
# ===================================================================
def update_chat_on_post_save(sender, **kwargs):
    """When a Post object is created, set its parent Chat object's
    updated time to now."""
    if kwargs['created']:
        post = kwargs['instance']
        post.parent.updated = datetime.datetime.now()
        post.parent.save()

# Wire up the signals to their models
post_save.connect(update_chat_on_post_save, sender=Post)
