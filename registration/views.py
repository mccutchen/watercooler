from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.template import RequestContext

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

    return render_to_response("registration/register.html", {'form':form}, \
        context_instance=RequestContext(request))
