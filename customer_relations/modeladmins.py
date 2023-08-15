from django.contrib import admin
from .models import *

@admin.register(Officer)
class OfficerModelAdmin(admin.ModelAdmin):
    list_display = ('account',)


@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ( 'message_category', 'student_account', 'student', 'settled')
    list_filter = ('settled', 'message_category',)


admin.site.register(MessageCategory)

