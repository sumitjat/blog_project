from django.contrib import admin
from app.models import Post,Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','created','publish','updated','status']

    # we want to filter in admin
    list_filter = ('status',)

    # for search option
    search_fields = ('title',)

    # we want data to choose from id field
    raw_id_fields = ('author',)

    # we can see navbar in admin
    date_hierarchy = 'publish'
    # to order
    ordering = ['status','publish']
    # we can slug to be set automatically based on other field
    prepopulated_fields = {'slug':('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','created','updated','active']
    list_filter = ('active',)


admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
