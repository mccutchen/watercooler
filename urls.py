from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.contrib.auth.views import login, logout
from django.contrib import admin

from models import Chat
from views import chat, post, create, register, ping

# These options dicts set up the front page (index) and public chat
# list views, which use Django's generic views and therefore do not
# have their own dedicated view functions in views.py.
index_options = {
    'template': 'index.html',
    'extra_context': {
        # Show the five most recently-updated chats on the front page
        'public_chats': lambda: Chat.objects.public()[:5],
    },
}
chat_list_options = {
    'queryset': Chat.objects.public().order_by('name'),
    'template_object_name': 'chat',
    'template_name': 'chat/chat_list.html',
}

# The URL patterns for Watercooler
urlpatterns = patterns('',
    # Essentially static pages
    url(r'^$', direct_to_template, index_options, name='index'),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}, name='about'),
    url(r'^contact/$', direct_to_template, {'template': 'contact.html'}, name='contact'),
    
    # Create a new chat
    url(r'^create/$', create, name='create'),

    # The list of public chats
    url(r'^chat/$', object_list, chat_list_options, name='chat_index'),

    # Views for individual chats, identified by their slug
    url(r'^chat/(?P<slug>[-\w]+)/$', chat, name='chat'),
    url(r'^chat/(?P<slug>[-\w]+)/post/', post, name='chat_post'),
    url(r'^chat/(?P<slug>[-\w]+)/ping/', ping, name='chat_ping'),

    # Authentication views (login and logout are provided by the
    # Django auth framework, register is provided in views.py)
    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/register/$', register),

    # The Django admin site
    (r'^admin/(.*)', admin.site.root),
)

# Automatically discover and install any admin sites (in this case,
# just the one admin.py)
admin.autodiscover()
