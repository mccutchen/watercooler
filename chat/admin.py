from django.contrib import admin
from chat.models import Chat, Post

class PostAdmin(admin.ModelAdmin):
    exclude = ('content_rendered',)
    list_display = ('user', 'timestamp', 'parent')

class PostInline(admin.StackedInline):
    model = Post
    exclude = ['content_rendered']

class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'created_by', 'is_public')
    list_filter = ('is_public',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PostInline]

admin.site.register(Chat, ChatAdmin)
admin.site.register(Post, PostAdmin)