from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


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


class Diagnosis(models.Model):
    """Model to store ML model diagnosis results for an image."""
    image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE, related_name="diagnosis")
    disease_type = models.CharField(
        max_length=50,
        choices=[
            ("pneumonia", "Pneumonia"),
            ("lung_opacity", "Lung opacity"),
            ("pneumothorax", "Pneumothorax"),
            ("pleural_effusion", "Pleural effusion"),
            ("unknown", "Unknown"),
            ("normal", "Normal"),
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


class AdminStats(models.Model):
    """Model to store aggregated statistics for admin use."""
    date = models.DateField(default=timezone.now)
    total_checks = models.PositiveIntegerField(default=0)
    most_common_disease = models.CharField(max_length=100, blank=True)
    most_common_disease_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        unique_together = ["date"]  # One stats entry per day

    def __str__(self):
        return f"Stats for {self.date}"

    @classmethod
    def update_daily_stats(cls, date):
        """Update or create stats for a given date."""
        checks = Diagnosis.get_daily_checks(date)
        common_disease = Diagnosis.get_most_common_disease()
        disease_name = common_disease["disease_type"] if common_disease else ""
        disease_count = common_disease["count"] if common_disease else 0

        stats, _ = cls.objects.update_or_create(
            date=date,
            defaults={
                "total_checks": checks,
                "most_common_disease": disease_name,
                "most_common_disease_count": disease_count,
            },
        )
        return stats