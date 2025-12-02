from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from chats.models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["user_id", "username", "email"]


admin.site.register(User, UserAdmin)
