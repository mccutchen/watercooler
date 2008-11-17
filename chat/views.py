from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from chat.models import Chat, Post

@login_required
def chat(request, slug):
    return object_detail(
        request,
        queryset=Chat.objects.all(),
        slug=slug,
        template_object_name='chat'
    )

@login_required
def post(request, slug):
    if request.POST:
        content = request.POST.get('content', '')
        chat = Chat.objects.get(slug=slug)
        post = Post(user=request.user, parent=chat, content=content)
        post.save()
    return HttpResponseRedirect(reverse('chat', args=[slug]))