from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Diagnosis
from images.models import UploadedImage
from .serializers import DiagnosisSerializer
from images.serializers import UploadedImageSerializer



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
