import datetime, time

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.defaultfilters import escape
from django.conf import settings


class ChatManager(models.Manager):
    """A custom manager for Chat objects, which adds a public() method
    that returns only public chats."""
    def public(self):
        """Returns only public chats."""
        return self.get_query_set().filter(is_public=True)

class Chat(models.Model):
    """Represents a single chat, which can contain many Posts.  Chats
    can be public or private and are identified by their slug in
    URLs."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    updated = models.DateTimeField(auto_now_add=True)

    # Use the custom manager defined above
    objects = ChatManager()

    class Meta:
        ordering = ('-updated', 'name', 'created')
        get_latest_by = 'updated'
        app_label = 'watercooler'

    def users(self):
        """Returns a dictionary containing a list of active users and
        a list of inactive users who have contributed to this chat."""

        # A user is inactive if they have not pinged in 20 seconds.
        cutoff = datetime.datetime.now() - \
            datetime.timedelta(0, settings.ACTIVE_USER_TIMEOUT)

        # A queryset containing each user who has contributed to this
        # chat.
        allusers = User.objects.filter(posts__parent__pk=self.id).distinct()

        # Pull get the active and inactive users from the queryset
        # based on the cutoff time determined above.
        active = [user for user in allusers if user.last_login > cutoff]
        inactive = [user for user in allusers if user.last_login < cutoff]
        return dict(active=active, inactive=inactive)

    @models.permalink
    def get_absolute_url(self):
        """Uses Django's built-in URL-reversing to determine the
        absolute URL for this Chat object based on the URLs defined in
        urls.py."""
        return ('chat', [self.slug])

    def __unicode__(self):
        return u'%s' % self.name


class Post(models.Model):
    """Represents a Post object, which has a Chat object as its
    parent.  Each post is associated with the user who created it.
    The content of a post is plain text."""
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
        """Turns this posts's created datetime.datetime object into a
        Unix timestamp."""
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
