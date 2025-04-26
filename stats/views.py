from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import AdminStats
from .serializers import AdminStatsSerializer


# Create your views here.
class AdminStatsView(generics.ListAPIView):
    """View admin statistics."""
    serializer_class = AdminStatsSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return AdminStats.objects.all()