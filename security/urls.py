from django.urls import path
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    # TokenVerifyView
)

from . import views

urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login'),
    path('token/verify/', views.VerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('register', views.UserRegisterView.as_view(), name='client_register'),

    path('contact', views.ContactView.as_view(), name='contact'),
    # path('envs', views.EnvsView.as_view(), name='envs'),

    path('password_reset', views.ResetPasswordView.as_view(), name='password_reset'),
    path('change_password', views.ChangePasswordView.as_view(), name='change_password'),
] 
