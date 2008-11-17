from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.template.defaultfilters import slugify

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
    return HttpResponseRedirect(chat_url(slug))

@login_required
def create(request):
    name = request.POST['name']
    slug = slugify(name)
    print 'Creating chat named "%s" with slug "%s"' % (name, slug)
    chat = Chat(name=name, slug=slug, is_public=True, created_by=request.user)
    chat.save()
    return HttpResponseRedirect(chat_url(slug))

def chat_url(slug):
    """Utility function that uses the reverse() function to generate the
    correct URL for the Chat object with the given slug."""
    return reverse('chat', args=[slug])