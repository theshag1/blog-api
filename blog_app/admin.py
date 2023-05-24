from django.contrib import admin
from .models import Blog, LikeDislike , Comment

# Register your models here.
admin.site.register(Blog)
admin.site.register(LikeDislike)
admin.site.register(Comment)
