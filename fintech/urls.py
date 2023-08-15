from django.urls import path, include
from .views import *

urlpatterns = [
    path('activate/', activate_account, name='activate-account')
]
