from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^chat/$', views.index),
    (r'^chat/([\w\-_]+)/$', views.chat),
    (r'^chat/([\w\-_]+)/post/$', views.post),
)