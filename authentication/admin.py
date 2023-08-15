from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Profile)

#admin.site.unregister(UserAccount)

#@admin.register(UserAccount)
class UserAccountModelAdmin(UserAdmin):
    list_display = ('username', 'full_name')
    search_fields = ('username', 'email')

#admin.site.unregister(UserAccount)
#admin.site.register(UserAccount, UserAccountModelAdmin)
