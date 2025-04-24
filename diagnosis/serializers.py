from rest_framework import serializers
from .models import UploadedImage, Diagnosis, AdminStats


class DiagnosisSerializer(serializers.ModelSerializer):
    """Serializer for Diagnosis model."""
    class Meta:
        model = Diagnosis
        fields = ["image", "disease_type", "diagnosed_at"]
        read_only_fields = ["image", "disease_type", "diagnosed_at"]


class UploadedImageSerializer(serializers.ModelSerializer):
    """Serializer for UploadedImage model, including associated diagnosis."""
    diagnosis = DiagnosisSerializer(read_only=True)

    def validate_image(self, value):
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError("Image file too large (max 5MB).")
        valid_extensions = [".jpg", ".jpeg", ".png"]
        ext = value.name.lower().rsplit(".", 1)[-1]
        if f".{ext}" not in valid_extensions:
            raise serializers.ValidationError("Only JPG and PNG files are allowed.")
        return value

    class Meta:
        model = UploadedImage
        fields = ["id", "user", "image", "uploaded_at", "created_at", "diagnosis"]
        read_only_fields = ["user", "uploaded_at", "created_at", "diagnosis"]


class AdminStatsSerializer(serializers.ModelSerializer):
    """Serializer for AdminStats model."""
    class Meta:
        model = AdminStats
        fields = ["date", "total_checks", "most_common_disease", "most_common_disease_count"]
        read_only_fields = ["date", "total_checks", "most_common_disease", "most_common_disease_count"]