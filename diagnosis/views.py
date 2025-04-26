from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from .models import UploadedImage, Diagnosis, AdminStats
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from django.urls import reverse
from .serializers import (UploadedImageSerializer, DiagnosisSerializer, AdminStatsSerializer, 
                            UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
                            PasswordResetRequestSerializer, PasswordResetConfirmSerializer)
class UserRegistrationView(generics.CreateAPIView):
    """Register a new user."""
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)
        return Response(
            {"message": "User registered successfully", "username": user.username},
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(generics.GenericAPIView):
    """Log in a user and return a token."""
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "username": user.username},
            status=status.HTTP_200_OK,
        )


class UploadImageView(generics.CreateAPIView):
    """Upload an image for diagnosis."""
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Trigger Celery task for ML processing (to be implemented)
        # from .tasks import process_image
        # process_image.delay(serializer.instance.id)
        return Response(
            {"message": "Image uploaded successfully", "id": serializer.instance.id},
            status=status.HTTP_201_CREATED,
        )


class SingleDiagnosisView(generics.RetrieveAPIView):
    """View a single diagnosis."""
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Diagnosis.objects.filter(image__user=self.request.user)


class DiagnosisHistoryView(generics.ListAPIView):
    """View user's diagnosis history."""
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedImage.objects.filter(user=self.request.user).select_related("diagnosis")


class AdminStatsView(generics.ListAPIView):
    """View admin statistics."""
    serializer_class = AdminStatsSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return AdminStats.objects.all()

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset email sent."})

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset successful."})

class ImageDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UploadedImage.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise NotFound("Image not found or not owned by user.")
        return obj

class APIRootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        base_url = f"{request.scheme}://{request.get_host()}"
        endpoints = {
            "register": {
                "url": f"{base_url}{reverse('register')}",
                "description": "Register a new user (POST)"
            },
            "login": {
                "url": f"{base_url}{reverse('login')}",
                "description": "Authenticate user and get token (POST)"
            },            
            "logout": {
                "url": f"{base_url}{reverse('logout')}",
                "description": "Log out and invalidate token (POST, authenticated)"
            },
            "upload_image": {
                "url": f"{base_url}{reverse('upload_image')}",
                "description": "Upload an image for diagnosis (POST, authenticated)"
            },
            "diagnosis_history": {
                "url": f"{base_url}{reverse('diagnosis_history')}",
                "description": "View user's diagnosis history (GET, authenticated)"
            },
            "image_delete": {
                "url": f"{base_url}{reverse('image_delete', args=[1])}",
                "description": "Delete an uploaded image by ID (DELETE, authenticated)"
            },
            "single_diagnosis": {
                "url": f"{base_url}{reverse('single_diagnosis', args=[1])}",
                "description": "View a single diagnosis by ID (GET, authenticated)"
            },
            "admin_stats": {
                "url": f"{base_url}{reverse('admin_stats')}",
                "description": "View admin statistics (GET, admin only)"
            },
            "profile": {
                "url": f"{base_url}{reverse('profile')}",
                "description": "View or update user profile (GET/PATCH, authenticated)"
            },
            "password_reset_request": {
                "url": f"{base_url}{reverse('password_reset_request')}",
                "description": "Request a password reset email (POST)"
            },
            "password_reset_confirm": {
                "url": f"{base_url}{reverse('password_reset_confirm')}",
                "description": "Confirm password reset with token (POST)"
            }
        }
        return Response(endpoints)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."})