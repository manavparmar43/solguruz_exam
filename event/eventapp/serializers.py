from rest_framework import serializers
from eventapp.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password','is_superuser',"is_staff"]

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data["password"] = make_password(password)
        instance = super().create(validated_data)
        instance.save()
        return instance
    
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data["password"] = make_password(password)
        instance = super().create(validated_data)
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event_name',"event_location","event_city","event_date","event_time","event_owner",'event_create']


class EventInviteSerializer(serializers.ModelSerializer):


    class Meta:
        model = EventInvite
        fields = ['id', 'invite_user','invite_status',"invite_time","event","sender_user"]


class EventInviteListSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = EventInvite
        depth=2
        fields = ['id', 'invite_user','invite_status',"invite_time","event","sender_user"]
