from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='index'),
    url(r'^contact/$', direct_to_template, {'template': 'contact.html'}, name='contact'),
    (r'^chat/', include('chat.urls')),
    (r'^admin/(.*)', admin.site.root),
)
