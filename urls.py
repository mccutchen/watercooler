from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from chat.models import Chat

admin.autodiscover()

index_options = {
    'template': 'index.html',
    'extra_context': {
        'public_chats': Chat.objects.filter(is_public=True),
    },
}

urlpatterns = patterns('',
    url(r'^$', direct_to_template, index_options, name='index'),
    url(r'^contact/$', direct_to_template, {'template': 'contact.html'}, name='contact'),
    (r'^chat/', include('chat.urls')),
    (r'^admin/(.*)', admin.site.root),
)
