from django.contrib import admin

from users.models import User
from users.models import VerificationCode


# Register your models here.

@admin.register(VerificationCode)
class VerificationCode(admin.ModelAdmin):
    list_display = ['email', 'code', 'last_sent_time', 'is_verified']
    ordering = ['-last_sent_time']


admin.site.register(User)