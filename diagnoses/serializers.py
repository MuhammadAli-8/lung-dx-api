from rest_framework import serializers
from .models import Diagnosis


class DiagnosisSerializer(serializers.ModelSerializer):
    """Serializer for Diagnosis model."""
    class Meta:
        model = Diagnosis
        fields = ["image", "disease_type", "diagnosed_at"]
        read_only_fields = ["image", "disease_type", "diagnosed_at"]
