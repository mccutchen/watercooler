from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from watercooler.chat.models import Chat

info_dict = {
    'queryset': Chat.objects.all(),
    'template_object_name': 'chat',
}

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', object_detail, info_dict, name='chat_detail'),
    #(r'^chat/$', views.index),
    #(r'^chat/([\w\-_]+)/$', views.chat),
    #(r'^chat/([\w\-_]+)/post/$', views.post),
)