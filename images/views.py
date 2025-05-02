from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UploadedImage
from rest_framework.exceptions import NotFound
from .serializers import UploadedImageSerializer, BatchImageUploadSerializer, BatchUploadResultSerializer
import os
import numpy as np
import json
from django.conf import settings
from .preprocessing import preprocess_image
from .model_loader import load_model
import cv2
import base64
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


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

class BatchUploadImagesView(generics.GenericAPIView):
    """Upload multiple images at once for diagnosis."""
    serializer_class = BatchImageUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):
        if not model:
            return Response({"error": "Model not loaded"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Validate input data
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Get all files from validated data
        image_files = serializer.validated_data['images']
        
        results = []
        
        for image_file in image_files:
            # Create temporary instance
            image_instance = UploadedImage(user=request.user, image=image_file)
            image_instance.save()
            
            try:
                # Preprocess image
                processed_image = preprocess_image(image_instance.image.path)
                
                # Predict with model
                prediction = model.predict(processed_image)
                pred_index = int(np.argmax(prediction))
                
                if not labels or str(pred_index) not in labels:
                    # Delete unsuccessful instance
                    image_instance.delete()
                    continue
                
                predicted_label = labels[str(pred_index)]
                
                # Save prediction to the database
                image_instance.disease_type = predicted_label
                image_instance.save()
                
                # Add to results
                results.append({
                    "id": image_instance.id,
                    "filename": os.path.basename(image_instance.image.name),
                    "prediction": predicted_label,
                })
            
            except Exception as e:
                # Delete unsuccessful instance and continue with other images
                image_instance.delete()
                results.append({
                    "filename": os.path.basename(image_file.name),
                    "error": str(e)
                })
        
        if not results:
            return Response({"error": "Failed to process any images"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Create response using the result serializer
        response_data = {
            "message": f"Processed {len(results)} images",
            "successful": len([r for r in results if "error" not in r]),
            "failed": len([r for r in results if "error" in r]),
            "results": results
        }
        
        result_serializer = BatchUploadResultSerializer(data=response_data)
        if result_serializer.is_valid():
            return Response(result_serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            # Fallback to raw response if serializer fails
            return Response(response_data, status=status.HTTP_201_CREATED)