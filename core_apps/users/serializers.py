from dj_rest_auth.registration.serializers import RegisterSerializer
from core_apps.profiles.models import Profile
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender", required=False)
    phonenumber = serializers.CharField(source="profile.phonenumber", required=False)
    profile_photo = serializers.ReadOnlyField(source="profile.profile_photo.url", required=False)
    country = CountryField(source='profile.country',required=False)
    city = serializers.CharField(source="profile.city", required=False)
    full_name = serializers.ReadOnlyField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:  
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "phonenumber",
            "profile_photo",
            "country",
            "city",
        ]
    def get_first_name(self, obj):
        return obj.first_name.title()

    def get_last_name(self, obj):
        return obj.last_name.title()

    def get_full_name(self, obj):
        first_name = obj.first_name.title()
        last_name = obj.last_name.title()
        return f"{first_name} {last_name}"
    
    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"]=True
        return representation

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "password": self.validated_data.get("password1", ""),
        })
        return data
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self)

        user.email = self.cleaned_data.get("email", "")
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.set_password(self.cleaned_data.get("password", ""))

        user.save()
        setup_user_email(request, user, [])
        
        return user