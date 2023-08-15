from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    #list_display = ('person1', 'person2',)
    #list_filter = ('person1', 'person2',)  
    pass

@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ('chat', 'message','time_sent')
