import re
from django.db import models
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
        """Before saving this post object, run its user-supplied content
        through a function that will look for URLs and turn them into
        links, images, embedded videos, etc."""
        
        # First, escape any HTML in the user's input
        safe_content = escape(self.content)
        
        # Next, run the escaped content through the renderer, which
        # will turn URLs into links, display images inline, etc.
        self.content_rendered = render_urls(safe_content)
        
        # Finally, save this post object.
        super(Post, self).save()
    
    def __unicode__(self):
        return 'Post by %s on %s' % (self.user, self.parent)


def render_urls(content):
    """Look for URLs in the content and turn them into HTML elements.
    URLs pointing to images or videos or sound file should be turned
    into inline representations of themselves.  All other URLs should
    be turned into links."""
    
    # Pattern to match any URL
    url_pattern = r'((http://|www\.){1,2}(www\.)?[A-z0-9\-.]+\.([A-z]{2,4}\.?)+[^\s]*)'
    
    # Patterns to match particular kinds of URLs
    img_pattern = r'\.(jpg|jpeg|gif|png)$'
    youtube_pattern = r'^http://www\.youtube\.com/watch\?v=([A-z0-9]{11})'
    audio_pattern = r'\.(mp3|aac)$'
    
    def replace(match):
        """Called for any string that matches the URL regex.  If the URL
        points to an image file, returns an HTML <img> element.  Otherwise
        returns an HTML <a> element."""
        url = match.group(1)
        
        # Ensure that the URL starts with http://
        url = re.match(r'^https?://', url) and url or 'http://%s' % url
        
        # Context dict that will be used to render the snippet that
        # is chosen
        context = {
            'url': url,
            'MEDIA_URL': settings.MEDIA_URL,
        }
        
        # Are we looking at the URL of an image file?
        if re.search(img_pattern, url, re.IGNORECASE):
            template = 'image'
        
        # Are we looking at the URL of a YouTube video?
        elif re.search(youtube_pattern, url, re.IGNORECASE):
            vid = re.search(youtube_pattern, url).group(1)
            context['vid'] = vid
            template = 'youtube'
        
        # Are we looking at the URL of an mp3 file?
        elif re.search(audio_pattern, url, re.IGNORECASE):
            template = 'audio'
            
        # None of the above? Just create a normal link.
        else:
            template = 'link'
        
        return render_to_string('chat/snippets/%s.html' % template, context)
    
    # Make the substitution and return the result
    return re.sub(url_pattern, replace, content)
