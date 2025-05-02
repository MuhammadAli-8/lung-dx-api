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

class BatchImageUploadSerializer(serializers.Serializer):
    """Serializer for handling multiple image uploads."""
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000, allow_empty_file=False, use_url=False),
        required=True,
        help_text="Select multiple image files for batch diagnosis"
    )
    
    def validate_images(self, images):
        """Validate the list of image files."""
        # Check if we have any images
        if not images:
            raise serializers.ValidationError("No images provided")
        
        # Check number of images
        if len(images) > 100:  # Limit to 10 images per batch
            raise serializers.ValidationError("Maximum 100 images allowed per batch upload")
            
        # Validate file types
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/dicom']
        for image in images:
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise serializers.ValidationError(f"Unsupported file type: {image.content_type}. Supported types are JPEG, PNG, and DICOM.")
                
        # Validate file size (limit to 10MB per file)
        max_size = 10 * 1024 * 1024  # 10MB
        for image in images:
            if image.size > max_size:
                raise serializers.ValidationError(f"Image file too large. Maximum size is 10MB.")
                
        return images
    
    class Meta:
        """Meta class for documentation."""
        swagger_schema_fields = {
            "title": "Batch Image Upload",
            "description": "Upload multiple images at once for lung disease diagnosis"
        }

class BatchUploadResultSerializer(serializers.Serializer):
    """Serializer for batch upload response."""
    message = serializers.CharField()
    successful = serializers.IntegerField()
    failed = serializers.IntegerField()
    results = serializers.ListField(child=serializers.DictField())
