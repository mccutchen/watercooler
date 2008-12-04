import datetime, operator, time
import simplejson as json

from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template.defaultfilters import force_escape, slugify
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from models import Chat, Post

@login_required
@never_cache
def chat(request, slug):
    chat = get_object_or_404(Chat, slug=slug)
    posts = chat.posts.all()
    
    # Get a list of the active and inactive users for this chat, and
    # make sure that the current user is in the active list (which
    # they won't be by default if they have not yet contributed)
    users = chat.users()
    if request.user not in users['active']:
        users['active'].append(request.user)
    if request.user in users['inactive']:
        users['inactive'].remove(request.user)

    context = {
        'chat': chat,
        'posts': posts,
        'users': users,
    }
    return direct_to_template(request, 'chat/chat.html', context)

@login_required
def post(request, slug):
    chat = get_object_or_404(Chat, slug=slug)
    if request.POST:
        content = request.POST.get('content', '')
        post = Post(user=request.user, parent=chat, content=content)
        post.save()

        # Update the user's last ping value
        user_ping(request.user)

        if request.is_ajax():
            response = json.dumps({
                'timestamp': post.timestamp(),
                'content': force_escape(post.content),
            })
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

@login_required
def ping(request, slug):
    """This is the Ajax polling endpoint.  An Ajax request will be made
    containing the latest timestamp on the client side.  The response
    will be a JSON object containing the posts made in the interim and
    a list of active and inactive users."""
    chat = get_object_or_404(Chat, slug=slug)
    if request.POST:
        # Log the ping time for this user
        user_ping(request.user)

        # Increasing the timestamp by one second eliminates duplicates
        # on the client side.  This probably merits further thought.
        latest_timestamp = float(request.POST.get('latest', time.time())) + 1
        latest = datetime.datetime.fromtimestamp(latest_timestamp)

        # Get a list of posts that were made after the latest time
        # given by the client
        posts_needed = chat.posts.select_related('user').filter(created__gt=latest)

        # The response to be serialized as JSON
        response = dict(posts=[], active_users=[], inactive_users=[])

        # Fill in the response with posts and users
        for post in posts_needed:
            response['posts'].append({
                'user': post.user.username,
                'content': post.content,
                'timestamp': post.timestamp(),
            })

        # Add active and inactive users
        for status, users in chat.users().items():
            for user in users:
                response['%s_users' % status].append(user.username)

        # Make sure the current user is included, even it has not
        # contributed
        if request.user.username not in response['active_users']:
            response['active_users'].append(request.user.username)

        # Serialize the response as JSON
        return HttpResponse(json.dumps(response), mimetype='application/json')

    return HttpResponseServerError()

@login_required
def filterchat(request, slug):
    """Filters a chat by username and/or keyword.  Filtered chat views
    are static (ie, not dynamically updated via Ajax)."""
    chat = get_object_or_404(Chat, slug=slug)
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
        'users': chat.users(),
        'filters': filters,
    }
    return direct_to_template(request, 'chat/filter.html', context)

def register(request):
    """Register view, to go along with the login and logout views
    provided by Django's auth framework.  Registers a user and
    automatically logs them in."""
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user in the database
            new_user = form.save()
            # Log the user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            assert user is not None
            login(request, user)
            return HttpResponseRedirect(request.POST.get('next', '/'))

    # We're either displaying the form for the first time (GET rather
    # than POST) or the form was invalid (duplicate username,
    # mismatched passwords, etc.).
    next = request.GET.get('next')
    context = { 'form': form, 'next': next }
    return direct_to_template(request, "registration/register.html", context)


# ====================================================================
# Utility functions
# ====================================================================
def user_ping(user):
    """Updates the given user's last_login to the current time.  Used
    to determine which users are still actively participating in a
    chat."""
    user.last_login = datetime.datetime.now()
    user.save()

def chat_url(slug):
    """Uses the reverse() function to generate the correct URL for the
    Chat object with the given slug."""
    return reverse('chat', args=[slug])
