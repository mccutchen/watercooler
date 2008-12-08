import datetime, operator, time
import simplejson as json

from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template.defaultfilters import force_escape, slugify
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from django.contrib.auth.models import User
from models import Chat, Post


# ====================================================================
# Chat views.  Users must be logged in to access these views.  All
# chats are identified by their slug in the URL.
# ====================================================================
@login_required
@never_cache
def chat(request, slug):
    """Displays an ongoing conversation, which will be updated live
    via Ajax.

    FIXME: Not really sure about this, but this view is never cached
    to help deal with layout problems."""
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
    """Adds a post to the chat identified by the given slug.  Also
    updates the current user's latest ping time, reflecting activity
    in this chat.

    This view will handle either normal POSTs or POSTs via Ajax (in
    which case it returns a JSON response with the timestamp of the
    created post and the post's HTML-escaped content."""
    chat = get_object_or_404(Chat, slug=slug)
    if request.POST:
        content = request.POST.get('content', '')
        post = Post(user=request.user, parent=chat, content=content)
        post.save()

        # Update the user's last ping value to reflect active
        # participation in this chat.
        user_ping(request.user)

        # If we're processing an Ajax request, return the timestamp of
        # the post we just created and its HTML-escaped content in
        # JSON format.
        if request.is_ajax():
            response = json.dumps({
                'timestamp': post.timestamp(),
                'content': force_escape(post.content),
            })
            return HttpResponse(response, mimetype='application/json')

    # Redirect the user back to this chat's page for normal, non-Ajax
    # requests.
    return HttpResponseRedirect(chat.get_absolute_url())

@login_required
def create(request):
    """Creates a new chat object.

    FIXME: If the given name is taken, this will just silently
    redirect the user to the already-created chat with that name
    without telling them that they did not create a new chat."""
    name = request.POST.get('name')
    if not name:
        return HttpResponseRedirect(reverse('index'))
    slug = slugify(name)
    chat = Chat(name=name, slug=slug, is_public=True, created_by=request.user)
    try:
        chat.save()
    except:
        # For now, if a chat with the same slug has already been created
        # just silently redirect to that chat.
        pass

    # Redirect the user to the URL for their new chat.
    return HttpResponseRedirect(chat.get_absolute_url())

@login_required
def ping(request, slug):
    """The Ajax polling endpoint.  Accepts Ajax requests containing
    the timestamp of the latest post on the client side.  Responds
    with a JSON object containing the posts made since that timestamp
    and a list of active and inactive users."""
    chat = get_object_or_404(Chat, slug=slug)
    if request.POST:
        # Update the ping time for this user
        user_ping(request.user)

        # Turn the latest timestamp given by the client into a
        # datetime object for querying the database. FIXME: The
        # timestamp needs to be increased by one second to eliminate
        # duplicates.  This seems like a bug to me, but it works.
        latest_timestamp = float(request.POST.get('latest', time.time())) + 1
        latest = datetime.datetime.fromtimestamp(latest_timestamp)

        # Get a list of posts that were made after the latest time
        # given by the client.  Selects the related user objects in
        # the same query, for efficiency.
        posts_needed = chat.posts.select_related('user').filter(created__gt=latest)

        # The structure of the response to be serialized as JSON.
        response = dict(posts=[], active_users=[], inactive_users=[])

        # Add the needed posts to the response.
        for post in posts_needed:
            response['posts'].append({
                'user': post.user.username,
                'content': post.content,
                'timestamp': post.timestamp(),
            })

        # Add active and inactive users.
        for status, users in chat.users().items():
            for user in users:
                response['%s_users' % status].append(user.username)

        # Make sure the current user is included, even it has not
        # contributed.
        if request.user.username not in response['active_users']:
            response['active_users'].append(request.user.username)

        # Serialize the response as JSON
        return HttpResponse(json.dumps(response), mimetype='application/json')

    # Requests to this view must be made via POST.
    return HttpResponseNotAllowed(['POST'])

@login_required
def filterchat(request, slug):
    """Filters a chat by username and/or keyword.  Filtered chat views
    are static (ie, not dynamically updated via Ajax).  So-named to
    avoid clobbering the built-in Python filter function."""
    chat = get_object_or_404(Chat, slug=slug)
    posts = chat.posts.all()

    # Tells the template which filters are in effect.
    filters = {}

    # Optionally filter posts by keyword (simplistic search)
    # From: http://toastdriven.com/fresh/quick-dirty-search-django/
    q = request.GET.get('q')
    if q:
        terms = [term.strip() for term in q.split()]
        q_objects = []
        for term in terms:
            q_objects.append(Q(content__icontains=term))
        # Combine Q objects into a clause with OR
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


# ====================================================================
# Registration views (the login and logout views are provided by
# Django's auth framework)
# ====================================================================
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
            login(request, user)
            return HttpResponseRedirect(request.POST.get('next', '/'))

    # We're either displaying the form for the first time (GET rather
    # than POST) or the form was invalid (duplicate username,
    # mismatched passwords, etc.).
    next = request.GET.get('next')
    context = { 'form': form, 'next': next }
    return direct_to_template(request, "registration/register.html", context)

def username_available(request, username):
    """Checks to see if the given username is available for
    registration.  Returns 1 if it is, 0 if not."""
    try:
        User.objects.get(username=username)
        result = '0'
    except User.DoesNotExist:
        result = '1'
    # Return the result as text/plain
    return HttpResponse(result, mimetype='text/plain')


# ====================================================================
# Utility functions
# ====================================================================
def user_ping(user):
    """Updates the given user's last_login to the current time.  Used
    to determine which users are still actively participating in a
    chat."""
    user.last_login = datetime.datetime.now()
    user.save()
