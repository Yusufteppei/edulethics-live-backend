from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from .models import UserAccount, Profile

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'password', 'is_staff', 'is_executive')


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
