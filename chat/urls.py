from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail

from chat.views import chat_detail, post

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', chat_detail, name='chat_detail'),
    url(r'^(?P<slug>[-\w]+)/post/', post, name='chat_post'),
    #(r'^chat/$', views.index),
    #(r'^chat/([\w\-_]+)/$', views.chat),
    #(r'^chat/([\w\-_]+)/post/$', views.post),
)