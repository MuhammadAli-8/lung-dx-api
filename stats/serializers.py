from rest_framework import serializers
from .models import AdminStats

class AdminStatsSerializer(serializers.ModelSerializer):
    """Serializer for AdminStats model."""
    class Meta:
        model = AdminStats
        fields = ["date", "total_checks", "most_common_disease", "most_common_disease_count"]
        read_only_fields = ["date", "total_checks", "most_common_disease", "most_common_disease_count"]