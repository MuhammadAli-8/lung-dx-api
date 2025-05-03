from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse


class APIRootView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = None

    def get(self, request, *args, **kwargs):
        base_url = f"{request.scheme}://{request.get_host()}"
        endpoints = {
            "register": {
                "url": f"{base_url}{reverse('user:register')}",
                "description": "Register a new user (POST)"
            },
            "login": {
                "url": f"{base_url}{reverse('user:login')}",
                "description": "Authenticate user and get token (POST)"
            },            
            "logout": {
                "url": f"{base_url}{reverse('user:logout')}",
                "description": "Log out and invalidate token (POST, authenticated)"
            },
            "profile": {
                "url": f"{base_url}{reverse('user:profile')}",
                "description": "View or update user profile (GET/PATCH, authenticated)"
            },
            "password_reset_request": {
                "url": f"{base_url}{reverse('user:password_reset_request')}",
                "description": "Request a password reset email (POST)"
            },
            "password_reset_confirm": {
                "url": f"{base_url}{reverse('user:password_reset_confirm')}",
                "description": "Confirm password reset with token (POST)"
            },
            "upload_image": {
                "url": f"{base_url}{reverse('images:upload_image')}",
                "description": "Upload an image for diagnosis (POST, authenticated)"
            },
            "upload_multiple_images": {
                "url": f"{base_url}{reverse('images:batch-upload-images')}",
                "description": "Upload multiple images for diagnosis (POST, authenticated)"
            },
            "delete_image": {
                "url": f"{base_url}{reverse('images:delete_image', args=[1])}",
                "description": "Delete an uploaded image by ID (DELETE, authenticated)"
            },
            "diagnosis_history": {
                "url": f"{base_url}{reverse('images:diagnosis_history')}",
                "description": "View user's diagnosis history (GET, authenticated)"
            },
            "single_diagnosis": {
                "url": f"{base_url}{reverse('images:single_diagnosis', args=[1])}",
                "description": "View a single diagnosis by ID (GET, authenticated)"
            },
            "admin_stats": {
                "url": f"{base_url}{reverse('stats:admin_stats')}",
                "description": "View admin statistics (GET, admin only)"
            },
        }
        return Response(endpoints)

