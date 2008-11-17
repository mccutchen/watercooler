from django.shortcuts import render_to_response as django_render_to_response
from django.template import RequestContext

def render_to_response(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)
    return django_render_to_response(*args, **kwargs)
