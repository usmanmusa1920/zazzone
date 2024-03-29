from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    

class PostAdmin(admin.ModelAdmin):
    search_fields = ('publisher', 'pub_date', 'title', 'image', 'last_modified', 'text', 'code',)
    ordering = ('-last_modified',)
    list_filter = ('publisher', 'pub_date', 'title', 'last_modified')
    list_display = ('publisher', 'pub_date', 'last_modified', 'title', 'last_modified')
    
    fieldsets = (
        (None, {"fields": ('publisher', 'title', 'image', 'text', 'code', 'likers',), }),
        ('Date Information', {'fields': ('pub_date',)}),
    )

    inlines = [CommentInline]
    

admin.site.register(Post, PostAdmin)
