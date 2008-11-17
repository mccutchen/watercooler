from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail

from chat.views import chat, post, create

urlpatterns = patterns('',
    url(r'^create/$', create, name='chat_create'),
    url(r'^(?P<slug>[-\w]+)/$', chat, name='chat'),
    url(r'^(?P<slug>[-\w]+)/post/', post, name='chat_post'),
    #(r'^chat/$', views.index),
    #(r'^chat/([\w\-_]+)/$', views.chat),
    #(r'^chat/([\w\-_]+)/post/$', views.post),
)