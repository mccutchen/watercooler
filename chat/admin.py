from django.contrib import admin
from watercooler.chat.models import Chat, Post

class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'created_by', 'is_public')
    list_filter = ('is_public',)
    prepopulated_fields = {'slug': ('name',)}

class PostAdmin(admin.ModelAdmin):
    exclude = ('content_rendered',)
    list_display = ('user', 'timestamp', 'parent')

admin.site.register(Chat, ChatAdmin)
admin.site.register(Post, PostAdmin)