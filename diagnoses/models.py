from django.db import models
from django.utils import timezone
from images.models import UploadedImage

# Create your models here.
class Diagnosis(models.Model):
    """Model to store ML model diagnosis results for an image."""
    image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE, related_name="diagnosis")
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
    diagnosed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-diagnosed_at"]

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
