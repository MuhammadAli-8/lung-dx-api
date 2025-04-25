from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from .models import UploadedImage, Diagnosis, AdminStats
from .serializers import UploadedImageSerializer, DiagnosisSerializer, AdminStatsSerializer, UserRegistrationSerializer, UserLoginSerializer

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