from django.contrib import admin
from .models import UploadedImage

# Register your models here.
@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ("user", "image", "uploaded_at", "disease_type")
    list_filter = ("uploaded_at", "disease_type")
    search_fields = ("user__username", "disease_type")