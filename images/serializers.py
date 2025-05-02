from rest_framework import serializers
from .models import UploadedImage

class UploadedImageSerializer(serializers.ModelSerializer):
    """Serializer for UploadedImage model, including associated diagnosis."""
    
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
        fields = ["id", "user", "image", "uploaded_at", "created_at", "disease_type"]
        read_only_fields = ["user", "uploaded_at", "created_at", "disease_type"]