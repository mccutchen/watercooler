from django.contrib import admin
from models import Chat, Post

class PostAdmin(admin.ModelAdmin):
    """Sets up an admin interface for Post objects."""
    list_display = ('user', 'created', 'parent')
    list_filter = ('user', 'created', 'parent')
    date_hierarchy = 'created'
    search_fields = ('content',)

class PostInline(admin.StackedInline):
    """Allows Post objects to be edited inline on the admin pages for
    their parent Chat objects."""
    model = Post

class ChatAdmin(admin.ModelAdmin):
    """Sets up an admin interface for Chat objects that automatically
    prepopulates the slug field based on the name given to the chat.
    Posts for a given chat can be edited inline."""
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'created', 'created_by', 'is_public')
    list_filter = ('is_public', 'created', 'created_by')
    date_hierarchy = 'created'
    search_fields = ('name',)
    inlines = [PostInline]

admin.site.register(Chat, ChatAdmin)
admin.site.register(Post, PostAdmin)
