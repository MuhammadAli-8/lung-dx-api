from django.db import models
from user.models import User
from django.utils import timezone


# Create your models here.
class UploadedImage(models.Model):
    """Model to store user-uploaded images for diagnosis."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="lung_images/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image by {self.user.username} at {self.uploaded_at}"
