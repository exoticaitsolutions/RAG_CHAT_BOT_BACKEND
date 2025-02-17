from RAG_Backend import settings
from django.urls import path, re_path

from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.AdminDashboardController import AdminDashboardController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.AuthController import AuthController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.AuthProfileController import ProfileSettingController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.ForgetPasswordController import ForgetPasswordController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.ChatBot.ChatBotController import ChatBotController

urlpatterns = [

]
admin_auth_urls = [
    path('register/', AuthController().auth_register_page, name='register'),
    path('login/', AuthController().auth_login_page, name='login'),
    # Forget Password page 
    path("forget-password/", ForgetPasswordController().forget_password_page, name="forget-password"),
]

admin_dashboard_urls = [
path("dashboard/profile/<str:user_uuid>/setting-account/", ProfileSettingController().SettingProfileAccount, name="admin.profile.setting"),

# Admin Dashboards 
path("dashboard/", AdminDashboardController().admin_dashboard_page, name="admin.dashboard"),
# Create Chat Bot Functionaly 
path("user/<str:user_uuid>/chatbot/", ChatBotController().chatbot_dashboard_view, name="admin.user.chatbot"),
path('dashboard/chatbot/fetch-modal-content/', ChatBotController().fetch_modal_content, name='admin.fetch_modal_content_for_chat_bot'),

# Create Chabot INtergation 
path("dashboard/user/<str:user_uuid>/chatbot/<str:curd_type>", ChatBotController().handle_chatbot_action, name="admin.user.chatbot.manage"),

]
public_urls = [

]
api_urls = [

]
urlpatterns += admin_auth_urls + admin_dashboard_urls + public_urls + api_urls
# Serve media files in development
if settings.DEBUG:
    urlpatterns += settings.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)