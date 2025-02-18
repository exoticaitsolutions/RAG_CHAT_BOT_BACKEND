from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render,redirect
from RAG_CHATBOT_BACKEND_APIS.admin_view import login_required
from django.utils.decorators import method_decorator

from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.AuthController import AuthServices
from RAG_CHATBOT_BACKEND_APIS.models import Country
from RAG_CHATBOT_BACKEND_APIS.views import JsonResponse


class ProfileSettingController:
    """Controller for profile settings."""
    @method_decorator(login_required(login_url='/login/'))
    def SettingProfileAccount(self, request, user_uuid):
        country_list = Country.objects.all()  # Fetch all records with all fields
        login_user_uuid = request.user.uuid
        if request.method == "POST":
            form_data = request.POST
            profile_data = request.FILES
            if AuthServices.check_user_existence('uuid', login_user_uuid):
                # print('found')
                status , response = AuthServices.UpdateUser_Details(login_user_uuid,form_data,profile_data)
                if not status:
                    messages.error(request, "Something Is Wrong")
                messages.success(request, response)
                return redirect(f"/dashboard/profile/{login_user_uuid}/setting-account/")
            else:
                messages.error(request, "Something Is Wrong")
                return redirect("/login/")
        return render(request, "admin/auth/profile/accountSetting.html", 
        {"country_list": country_list ,"user":request.user})
    
    @method_decorator(login_required(login_url='/login/'))
    def SettingProfileSercurity(self, request, user_uuid):
        login_user_uuid = request.user.uuid
        if request.method == 'POST':
            form_data = request.POST
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user = request.user  # Get the currently logged-in user
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect(f"/dashboard/profile/{login_user_uuid}/setting-security/")
            elif user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully!")
                return redirect("/login/")
            else:
                messages.error(request, "Old password is incorrect")
                return redirect(f"/dashboard/profile/{login_user_uuid}/setting-security/")
        return render(request, "admin/auth/profile/change_password.html")