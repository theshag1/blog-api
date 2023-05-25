from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone")
        read_only_fields = ("id")


class UserSerializerr(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name", "last_name", "phone")


class UserUpdateSeriaslizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", 'username', 'age', 'adress')
        read_only_fields = ('id',)


class UserDetilSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone")
        read_only_fields = ("id",)


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.pop('password2')
        if password1 != password2:
            raise ValidationError(_("Password didn't match"))
        return super().validate(attrs)

    def create(self, validated_data):
        password1 = validated_data.pop("password1", None)
        user = User(**validated_data)
        user.set_password(password1)
        user.save()
        return user


class CustomTokenPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        data["user"] = UserSerializer(self.user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SendEmailVarificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChekEmailVarificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)
