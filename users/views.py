from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import Http404
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User, VerificationCode
from users.serializers import RegisterSerializer, LoginSerializer, UserSerializerr, UserDetilSerializer, \
    UserUpdateSeriaslizer
from users.serializers import SendEmailVarificationCodeSerializer, ChekEmailVarificationCodeSerializer


# Create your views here.

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = User.objects.filter(email=email).first()
        if user:
            authenticate(request, password=password, email=email)
            return Response(serializer.data)
        else:
            raise Http404


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializerr(request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = UserDetilSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmaiVerificationCode(APIView):
    @swagger_auto_schema(request_body=SendEmailVarificationCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendEmailVarificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = get_random_string(allowed_chars='123456789', length=6)
        varification_code, _ = (
            VerificationCode.objects.update_or_create(email=email, defaults={'code': code, 'is_verified': False})

        )
        varification_code.expired_at = varification_code.last_sent_time + timedelta(seconds=30)
        varification_code.save(update_fields=['expired_at'])
        subject = 'Verification code'
        email_user_name = email.split('@')[0]
        massage = f'Hi {email_user_name} 👋🏻, your email verifcation code is :{code}'
        send_mail(subject, massage, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
        return Response({'detil': 'Verification'})


class ChekEmailVerificaationCode(generics.CreateAPIView):
    queryset = VerificationCode.objects.all()
    serializer_class = ChekEmailVarificationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")
        verification_code = self.get_queryset().filter(email=email, is_verified=False).order_by(
            "-last_sent_time").first()
        if verification_code and verification_code.code != code and verification_code.is_expire:
            raise ValidationError("Verification code invalid.")
        verification_code.is_verified = True
        verification_code.save(update_fields=["is_verified"])
        return Response({"detail": "Verification code is verified."})


class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PUTCH']:
            return UserUpdateSeriaslizer
        return UserUpdateSeriaslizer
