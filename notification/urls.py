from .views import *
from django.urls import path, include


urlpatterns = [
        path('broadcasts/', broadcasts, name='notification'),
        path('has-viewed-all-broadcasts/', has_viewed_all_broadcasts, name='has-viewed-all-broadcasts')

]



