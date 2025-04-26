from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UploadedImage
from rest_framework.exceptions import NotFound
from .serializers import UploadedImageSerializer



# Create your views here.
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
