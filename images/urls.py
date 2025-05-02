from django.urls import path
from .views import UploadImageView, ImageDeleteView, DiagnosisHistoryView, SingleDiagnosisView, BatchUploadImagesView


app_name = 'images'
urlpatterns = [
    path("images/upload/", UploadImageView.as_view(), name="upload_image"),
    path("images/<int:pk>/", ImageDeleteView.as_view(), name="delete_image"),
    path("diagnoses/", DiagnosisHistoryView.as_view(), name="diagnosis_history"),
    path("diagnoses/<int:pk>/", SingleDiagnosisView.as_view(), name="single_diagnosis"),
    path('upload/batch/', BatchUploadImagesView.as_view(), name='batch-upload-images'),
]
