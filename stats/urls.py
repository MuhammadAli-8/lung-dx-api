from django.urls import path
from .views import AdminStatsView


app_name = 'stats'
urlpatterns = [
    path("stats/", AdminStatsView.as_view(), name="admin_stats"),
]
