from django.contrib.auth import get_user_model
from core_apps.users.serializers import UserSerializer, CustomRegisterSerializer
from rest_framework.exceptions import ValidationError
import pytest


User = get_user_model()

@pytest.mark.django_db
def test_user_serializer(normal_user):
    serializer = UserSerializer(normal_user)
    print(serializer.data)
    assert "id" in serializer.data
    assert "first_name" in serializer.data
    assert "last_name" in serializer.data
    assert "email" in serializer.data
    assert "city" in serializer.data
    assert "country" in serializer.data
    assert "gender" in serializer.data
    assert "phonenumber" in serializer.data

@pytest.mark.django_db
def test_to_representation_normal_user(normal_user):
    serializer = UserSerializer(normal_user)
    data_serializer = serializer.data
    assert "admin" not in data_serializer

@pytest.mark.django_db
def test_to_representation_super_user(super_user):
    serializer = UserSerializer(super_user)
    data_serializer = serializer.data
    assert "admin" in data_serializer
    assert data_serializer["admin"] is True

@pytest.mark.django_db
def test_custom_register_serializer(mock_request):
    valid_data = {
        "first_name":"mahsa",
        "last_name":"sh",
        "email": "dfdfdfdfzohdi@gmail.com",
        "password1":"test@56789",
        "password2":"test@56789",
    }
    serializer = CustomRegisterSerializer(data = valid_data)
    assert serializer.is_valid()

    user = serializer.save(mock_request)
    assert user.first_name == valid_data["first_name"]
    assert user.last_name == valid_data["last_name"]
    assert user.email == valid_data["email"]
    
    invalid_data = {
        "first_name":"mahsa",
        "last_name":"sh",
        "email": "zohdi@gmail.com",
        "password1":"12345678",
        "password2":"123",
    }

    serializer = CustomRegisterSerializer(data=valid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
