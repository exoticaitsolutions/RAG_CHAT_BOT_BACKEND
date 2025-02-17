from django.shortcuts import render
from RAG_CHATBOT_BACKEND_APIS.admin_view import login_required
from django.utils.decorators import method_decorator


class ProfileSettingController:
    """Controller for profile settings."""
    @method_decorator(login_required(login_url='/login/'))
    def SettingProfileAccount(self, request, user_uuid):
        return render(request, "admin/auth/profile/accountSetting.html")
