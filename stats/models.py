from django.db import models
from django.utils import timezone
from images.models import UploadedImage

# Create your models here.
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
        checks = UploadedImage.get_daily_checks(date)
        common_disease = UploadedImage.get_most_common_disease()
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