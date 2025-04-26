
from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UploadImageView,
    DiagnosisHistoryView, SingleDiagnosisView, AdminStatsView,
    UserProfileView, PasswordResetRequestView, PasswordResetConfirmView,
    APIRootView,ImageDeleteView, LogoutView
)

urlpatterns = [
        path("", APIRootView.as_view(), name="api_root"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("images/upload/", UploadImageView.as_view(), name="upload_image"),
    path("images/", DiagnosisHistoryView.as_view(), name="diagnosis_history"),
    path("images/<int:pk>/", ImageDeleteView.as_view(), name="image_delete"),
    path("diagnoses/<int:pk>/", SingleDiagnosisView.as_view(), name="single_diagnosis"),
    path("stats/", AdminStatsView.as_view(), name="admin_stats"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
