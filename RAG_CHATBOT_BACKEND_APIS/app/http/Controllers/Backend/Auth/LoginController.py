import re
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout, authenticate, login
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import User

from RAG_CHATBOT_BACKEND_APIS.models import CustomUser  # Update if using a custom model
# Set up logging
logger = logging.getLogger(__name__)

class LoginController(View):

    def get(self, request):
        return render(request, 'admin/auth/login.html')

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        data = request.POST
        username_or_email = data.get("username_or_address")
        password = data.get("password")

        if not username_or_email or not password:
            return JsonResponse({"status": "failed", "message": "Username or Email and password are required."})

        # Check if input is email or username
        if CustomUser.objects.filter(email=username_or_email).exists():
            user = User.objects.get(email=username_or_email)
            username = user.username
        else:
            username = username_or_email

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            url = '/dashboard/home/'
            return JsonResponse({"status": "success", "message": "User logged in successfully!", "redirect_url": url}, status=200)
        else:
            return JsonResponse({"status": "failed", "message": "Invalid username or password."})