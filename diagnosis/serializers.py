from rest_framework import serializers
from .models import UploadedImage, Diagnosis, AdminStats, User
from django.contrib.auth import authenticate


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

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        data["user"] = user
        return data