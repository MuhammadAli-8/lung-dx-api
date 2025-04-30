from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "email", "is_staff", "phone_number", "age")
    search_fields = ("email",)
