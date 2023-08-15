from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Profile
User = get_user_model()
