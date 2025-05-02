from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UploadedImage
from rest_framework.exceptions import NotFound
from .serializers import UploadedImageSerializer
import os
import numpy as np
import json
from django.conf import settings
from .preprocessing import preprocess_image
from .model_loader import load_model
import cv2
import base64


# Load model and labels
try:
    model = load_model(settings.BASE_DIR / 'images/lung_disease_model_final.h5')
    with open(settings.BASE_DIR / 'images/labels.json', 'r') as f:
        labels = json.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    labels = {}

class UploadImageView(generics.CreateAPIView):
    """Upload an image for diagnosis."""
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not model:
            return Response({"error": "Model not loaded"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer.save(user=self.request.user)
        image_instance = serializer.instance
        image_path = image_instance.image.path

        # Preprocess image
        processed_image = preprocess_image(image_path)

        # Predict with single input
        prediction = model.predict(processed_image)
        pred_index = int(np.argmax(prediction))
        if not labels or str(pred_index) not in labels:
            return Response({"error": "Invalid prediction index or empty labels"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        predicted_label = labels[str(pred_index)]

        # Save prediction to the database
        image_instance.disease_type = predicted_label
        image_instance.save()

        return Response({
            "message": "Image uploaded and processed successfully",
            "id": image_instance.id,
            "prediction": predicted_label,
        }, status=status.HTTP_201_CREATED)

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

class SingleDiagnosisView(generics.RetrieveAPIView):
    """View a single diagnosis."""
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedImage.objects.filter(user=self.request.user)

class DiagnosisHistoryView(generics.ListAPIView):
    """View user's diagnosis history."""
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedImage.objects.filter(user=self.request.user)

class MultipleImageUploadView(APIView):
    """Upload multiple images for diagnosis."""
    pass