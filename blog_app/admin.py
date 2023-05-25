from django.contrib import admin
from .models import Blog, LikeDislike, Comment

# Register your models here.
admin.site.register(Blog)


@admin.register(LikeDislike)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'type']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog']
