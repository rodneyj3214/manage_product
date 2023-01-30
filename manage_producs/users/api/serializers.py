from django.contrib.auth import authenticate, get_user_model, password_validation
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    """Generic User Model Serializer"""

    class Meta:
        model = User
        fields = ["username", "name", "email"]


class UserExtraSerializer(UserModelSerializer):
    """Custom User Model serializer with url for detail"""

    class Meta(UserModelSerializer.Meta):
        fields = ["username", "name", "url", "email"]
        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=64)

    def validate(self, data):
        """Validate Credentials"""
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        self.context["user"] = user
        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context["user"])
        return self.context["user"], token.key


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Validate Password and password_confirmation are the same"""
        password = data["password"]
        password_confirmation = data["password_confirmation"]
        if password != password_confirmation:
            raise serializers.ValidationError("Password dont match")
        password_validation.validate_password(password)
        return data

    def create(self, data):
        """Custom create function without password_confirmation field"""
        data.pop("password_confirmation")
        user = User.objects.create_user(**data, is_superuser=True)
        return user
