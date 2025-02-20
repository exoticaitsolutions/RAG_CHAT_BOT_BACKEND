from django.contrib import messages
from django.shortcuts import redirect, render
from RAG_CHATBOT_BACKEND_APIS.app.services.Auth.AuthServices import AuthServices
from django.contrib.auth import logout, authenticate, login

class AuthController:
    def auth_register_page(self, request):
        if request.method == "POST":
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if not all([username, email, password1, password2]):
                messages.error(request, "All fields are required.")
            elif password1 != password2:
                messages.error(request, "Passwords do not match!")
            elif AuthServices.check_user_existence('username', username):
                messages.error(request, "Username is already taken.")
            elif AuthServices.check_user_existence('email', email):
                messages.error(request, "Email is already registered.")
            else:
                status ,message= AuthServices.RegisterUser(username,email,password1)
                if not status:
                    messages.error(request, message)
                messages.success(request, message)
                return redirect("/login/")
            return redirect("/register/")
        return render(request, "admin/auth/register.html")
    
    def auth_login_page(self, request):
        if request.method == "POST":
            username_or_address = request.POST.get("username_or_address", "").strip()
            password = request.POST.get("password")
            if AuthServices.check_user_existence('email', username_or_address):
                user = AuthServices.fetch_user_data('email', username_or_address)
                username = user.username # type: ignore
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
