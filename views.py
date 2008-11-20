import operator
import simplejson as json

from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.template import RequestContext

from utils import render_to_response
from models import Chat, Post

@login_required
def chat(request, slug):
    chat = Chat.objects.get(slug=slug)
    posts = chat.posts.all()
    filters = {}
    
    # Optionally filter posts by keyword (simplistic search)
    # From: http://toastdriven.com/fresh/quick-dirty-search-django/
    q = request.GET.get('q')
    if q:
        terms = [term.strip() for term in q.split()]
        q_objects = []
        for term in terms:
            q_objects.append(Q(content__icontains=term))
        # Use operator's or_ to string together all of your Q objects.
        posts = posts.filter(reduce(operator.or_, q_objects))
        filters['search'] = q
    
    # Optionally filter posts by user name
    userfilter = request.GET.get('user')
    if userfilter:
        posts = posts.filter(user__username=userfilter)
        filters['user'] = userfilter
    
    context = {
        'chat': chat,
        'posts': posts,
        'filters': filters,
    }
    return render_to_response(request, 'chat/chat.html', context)

@login_required
def post(request, slug):
    if request.POST:
        content = request.POST.get('content', '')
        chat = Chat.objects.get(slug=slug)
        post = Post(user=request.user, parent=chat, content=content)
        post.save()
    
        if request.is_ajax():
            response = json.dumps({ 'timestamp': post.timestamp(), })
            return HttpResponse(response, mimetype='application/json')
    
    return HttpResponseRedirect(chat_url(slug))

@login_required
def create(request):
    name = request.POST.get('name')
    if not name:
        return HttpResponseRedirect(reverse('index'))
    slug = slugify(name)
    try:
        chat = Chat(name=name, slug=slug, is_public=True, created_by=request.user)
        chat.save()
    except:
        # For now, if a chat with the same slug has already been created
        # just silently redirect to that chat.
        pass
    return HttpResponseRedirect(chat_url(slug))

def chat_url(slug):
    """Utility function that uses the reverse() function to generate the
    correct URL for the Chat object with the given slug."""
    return reverse('chat', args=[slug])


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            assert user is not None
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()

    return render_to_response(request, "registration/register.html", {'form':form})