from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView,
    UserProfileView, PasswordResetRequestView, 
    PasswordResetConfirmView, LogoutView,
)


app_name = 'user'

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
