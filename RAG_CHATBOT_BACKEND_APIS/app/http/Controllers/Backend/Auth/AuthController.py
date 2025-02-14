import os
from django.contrib import messages
from django.shortcuts import redirect, render
from RAG_CHATBOT_BACKEND_APIS.models import CustomUser
from django.contrib.auth import logout, authenticate, login
from django.conf import settings
from RAG_CHATBOT_BACKEND_APIS.utils import format_name

class AuthController:
    def auth_register_page(self, request):
        if request.method == "POST":
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            formatted_username = format_name(str(username))
            user_upload_dir = os.path.join(settings.MEDIA_ROOT, formatted_username)
            user_chroma_db_dir = os.path.join(settings.MEDIA_ROOT, formatted_username)
            os.makedirs(user_upload_dir, exist_ok=True)
            os.makedirs(user_chroma_db_dir, exist_ok=True)
            if not all([username, email, password1, password2]):
                messages.error(request, "All fields are required.")
            elif password1 != password2:
                messages.error(request, "Passwords do not match!")
            elif CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
            else:
                CustomUser.objects.create_user(username=username, email=email, password=password1)
                messages.success(request, "User is Successfully  registered.")
                return redirect("/login/")
            return redirect("/register/")

        return render(request, "admin/auth/register.html")
    
    def auth_login_page(self, request):
        if request.method == "POST":
            username_or_address = request.POST.get("username_or_address", "").strip()
            password = request.POST.get("password")

            if CustomUser.objects.filter(email=username_or_address).exists():
                user = CustomUser.objects.get(email=username_or_address)
                username = user.username
            else:
                username = username_or_address

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard/")
            else:
                messages.error(request, "Invalid username/email or password.")
                return redirect("/login/")

        return render(request, "admin/auth/login.html")
    
    def auth_logoutSession(self, request):
        logout(request)  # Logs out the user and removes session data
        request.session.flush()  # Completely clears the session
        return redirect("/admin/auth/login/")  # Redirects to the login page
