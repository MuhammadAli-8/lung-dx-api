from django.contrib import admin
from .models import AdminStats

# Register your models here.
@admin.register(AdminStats)
class AdminStatsAdmin(admin.ModelAdmin):
    list_display = ("date", "total_checks", "most_common_disease", "most_common_disease_count")
    list_filter = ("date",)