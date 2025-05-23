from django.contrib import admin
from .models import Broadcast

# Register your models here.
@admin.register(Broadcast)
class BroadcastModelAdmin(admin.ModelAdmin):
    list_display = ('topic', 'category', 'time')
    list_filter = ('category',)
