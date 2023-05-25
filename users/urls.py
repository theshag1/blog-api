from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterView, LoginView, Profile, SendEmaiVerificationCode, ChekEmailVerificaationCode ,UserUpdateView
from users.soical_login.views import GoogleSocialAuthView , FacebookSocialAuthView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/faceobok/', FacebookSocialAuthView.as_view(), name='facebook_login'),
    path('auth/google/', GoogleSocialAuthView.as_view(), name='google_login'),
    path("profile/", Profile.as_view(), name='profile'),
    path("email/verification/", SendEmaiVerificationCode.as_view(), name='send-email'),
    path("email/verification/check", ChekEmailVerificaationCode.as_view(), name='check-email'),
    path("<int:pk>/update/", UserUpdateView.as_view(), name='check-email')

]
