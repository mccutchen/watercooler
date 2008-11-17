from django.db import models
from django.contrib.auth.models import User

class ChatManager(models.Manager):
    def public(self):
        return self.get_query_set().filter(is_public=True)

class Chat(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    
    # Use the custom manager defined above
    objects = ChatManager()
    
    class Meta:
        ordering = ('created',)
    
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
    content_rendered = models.TextField()
    
    class Meta:
        ordering = ('timestamp',)
        get_latest_by = 'timestamp'
        order_with_respect_to = 'parent'
    
    def save(self):
        self.content_rendered = self.content
        super(Post, self).save()
    
    def __unicode__(self):
        return 'Post by %s on %s' % (self.user, self.parent)