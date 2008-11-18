import re
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import escape

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
        # The special content renderers (which do things like turn URLs
        # into actual links) to run each post's content through
        renderers = [render_links]
        
        # First, escape any HTML in the user's input
        safe_content = escape(self.content)
        
        # Then, run the escaped content through each renderer
        for renderer in renderers:
            safe_content = renderer(safe_content)
        
        self.content_rendered = safe_content
        super(Post, self).save()
    
    def __unicode__(self):
        return 'Post by %s on %s' % (self.user, self.parent)


# From http://snipplr.com/view/2371/regex-regular-expression-to-match-a-url/
url_pattern = r'((https?://)?([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)'

def render_links(content):
    """Turn any URL-looking strings into actual HTML <a>
    elements."""
    
    def url_replace(match):
        """Called for any string that matches the URL regex.  Tries
        to ensure that the URL starts with 'http://'."""
        url = match.group(1)
        url = url if re.match(r'^https?://', url) else 'http://%s' % url
        return '<a href="%s">%s</a>' % (url, url)
        
    return re.sub(url_pattern, url_replace, content)
