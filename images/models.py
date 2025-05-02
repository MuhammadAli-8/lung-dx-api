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
        return f"Image by {self.user.username} at {self.uploaded_at}, with pk {self.pk}"
    disease_type = models.CharField(
        max_length=50,
        choices=[
            ("No Finding", "No Finding"),
            ("Pneumonia", "Pneumonia"),
            ("Pneumothorax", "Pneumothorax"),
            ("Effusion", "Effusion"),
            ("Cardiomegaly", "Cardiomegaly"),
        ],
        help_text="Diagnosis result from ML model"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.disease_type} for {self.image}"

    @classmethod
    def get_daily_checks(cls, date):
        """Return the number of diagnoses for a given date."""
        return cls.objects.filter(
            diagnosed_at__date=date
        ).count()

    @classmethod
    def get_most_common_disease(cls):
        """Return the most common disease type and its count."""
        return (
            cls.objects.values("disease_type")
            .annotate(count=models.Count("disease_type"))
            .order_by("-count")
            .first()
        )
