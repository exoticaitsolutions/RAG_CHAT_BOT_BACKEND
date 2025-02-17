# Simport logging
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from RAG_CHATBOT_BACKEND_APIS.models import *
logger = logging.getLogger(__name__)


@method_decorator(login_required(login_url='/login/'))
class ProfileSettingController:
    # Create Chat bot Api
    # @method_decorator(login_required(login_url='/login/'))
    def SettingProfileAccount(self, request,user_uuid):
        return render(request, 'admin/auth/profile/accountSetting.html')