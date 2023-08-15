from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *



urlpatterns = [
    path('message/', message, name='message'),
    path('chat/', chat, name='chat')
]
