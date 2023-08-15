from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet,username_available,email_available
from django.urls import include, path

from .views import *
router = DefaultRouter()

router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path("", include(router.urls)),
    path("username-available/", username_available, name='username-available'),
    path("email-available/", email_available, name='email-available'),
    path("signup/", signup, name='signup'),
    path("change-password-with-username", change_password_with_username, name="change-password-with-username"),
]
