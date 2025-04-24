from django.contrib import admin
from .models import User, UploadedImage, Diagnosis, AdminStats

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff")
    search_fields = ("username", "email")

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ("user", "image", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("user__username",)

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ("image", "disease_type", "diagnosed_at")
    list_filter = ("disease_type", "diagnosed_at")
    search_fields = ("disease_type",)

@admin.register(AdminStats)
class AdminStatsAdmin(admin.ModelAdmin):
    list_display = ("date", "total_checks", "most_common_disease", "most_common_disease_count")
    list_filter = ("date",)