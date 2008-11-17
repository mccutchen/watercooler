from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from chat.models import Chat

@login_required
def chat_detail(request, slug):
    return object_detail(
        request,
        queryset=Chat.objects.all(),
        slug=slug,
        template_object_name='chat'
    )