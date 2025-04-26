from rest_framework import serializers
from .models import UploadedImage, Diagnosis, AdminStats, User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode



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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        read_only_fields = ['username']

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email address.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        subject = "Password Reset Request"
        message = f"Click the link to reset your password: {reset_url}"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user ID.")
        
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid or expired token.")
        
        return data

    def save(self):
        uid = force_str(urlsafe_base64_decode(self.validated_data['uid']))
        user = User.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()