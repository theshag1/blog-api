from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterView, LoginView, Profile, SendEmaiVerificationCode, ChekEmailVerificaationCode

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("profile/", Profile.as_view(), name='profile'),
    path("email/verification/", SendEmaiVerificationCode.as_view(), name='send-email'),
    path("email/verification/check", ChekEmailVerificaationCode.as_view(), name='check-email')

]
