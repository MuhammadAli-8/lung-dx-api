from django_filters import rest_framework as filters
from .models import UploadedImage

class UploadedImageFilter(filters.FilterSet):
    disease_type = filters.CharFilter(lookup_expr='iexact')
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = UploadedImage
        fields = ['disease_type', 'created_at']