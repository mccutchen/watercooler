from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list

from models import Chat
from views import chat, post, create

chat_list_options = {
    'queryset': Chat.objects.public(),
    'template_object_name': 'chat',
}

urlpatterns = patterns('',
    url(r'^$', object_list, chat_list_options, name='chat_index'),
    url(r'^create/$', create, name='chat_create'),
    url(r'^(?P<slug>[-\w]+)/$', chat, name='chat'),
    url(r'^(?P<slug>[-\w]+)/post/', post, name='chat_post'),
)