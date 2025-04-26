from django.contrib import admin
from .models import Diagnosis




@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ("image", "disease_type", "diagnosed_at")
    list_filter = ("disease_type", "diagnosed_at")
    search_fields = ("disease_type",)