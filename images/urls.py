from django.urls import path
from .views import UploadImageView,ImageDeleteView


app_name = 'images'
urlpatterns = [
    path("images/upload/", UploadImageView.as_view(), name="upload_image"),
    path("images/<int:pk>/", ImageDeleteView.as_view(), name="delete_image"),
]
