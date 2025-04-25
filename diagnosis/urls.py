
from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UploadImageView,
    SingleDiagnosisView,
    DiagnosisHistoryView,
    AdminStatsView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("images/", DiagnosisHistoryView.as_view(), name="diagnosis_history"),
    path("images/upload/", UploadImageView.as_view(), name="upload_image"),
    path("diagnoses/<int:pk>/", SingleDiagnosisView.as_view(), name="single_diagnosis"),
    path("stats/", AdminStatsView.as_view(), name="admin_stats"),
]
