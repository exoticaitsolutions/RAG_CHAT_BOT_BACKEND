from django.urls.resolvers import URLPattern
from RAG_Backend import settings
from django.urls import path, re_path

from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.API.Chatbot.ChatbotQueryApiController import ChatbotQueryApiController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.AdminDashboardController import AdminDashboardController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.AuthController import AuthController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.AuthProfileController import ProfileSettingController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.ForgetPasswordController import ForgetPasswordController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.ResetPasswordController import ResetPasswordController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Modules.ChatBot.ChatBotController import ChatBotController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Modules.ChatBot.ChatbotDashboardController import ChatbotDashboardController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.ChatBotFrontendController import ChatBotFrontendController



urlpatterns = [

]
admin_auth_urls = [
    path('register/', AuthController().auth_register_page, name='register'),
    path('login/', AuthController().auth_login_page, name='login'),
    # Forget Password page 
    # Forget Password
    path("forget-password/", ForgetPasswordController().forget_password_page, name="forget-password"),
    
    # Reset Password
    path('reset-password/<uidb64>/<token>/', ResetPasswordController().reset_password_page,  name='reset_password'),
]

admin_dashboard_urls = [
# Dashboard URL 
path("dashboard/", AdminDashboardController().admin_dashboard_page, name="admin.dashboard"),
# Profile URLS 
path("dashboard/profile/<str:user_uuid>/setting-account/", ProfileSettingController().SettingProfileAccount, name="admin.profile.setting.profile"),
path("dashboard/profile/<str:user_uuid>/setting-security/", ProfileSettingController().SettingProfileSercurity, name="admin.profile.setting.security"),

# Create Chat Bot Functionaly 
path("dashboard/user/<str:user_uuid>/chatbot/", ChatBotController().chatbot_dashboard_view, name="admin.user.chatbot"),
path('dashboard/chatbot/fetch-modal-content/', ChatBotController().fetch_modal_content, name='admin.fetch_modal_content_for_chat_bot'),
path("dashboard/user/<str:user_uuid>/chatbot/post/<str:curd_type>", ChatBotController().handle_chatbot_action, name="admin.user.chatbot.manage"),
path("dashboard/user/<str:user_uuid>/chatbot/<str:chatbot_id>/<str:view_type>/", ChatbotDashboardController().view_chatbot_dashboard, name="admin.user.chatbot.dashboard"),
# Upload Documents Chatborad 
path("dashboard/user/<str:user_uuid>/chatbot/<str:chatbot_id>/upload/<str:upload_type>", ChatbotDashboardController().upload_and_start_training, name="admin.user.chatbot.upload-document"),

path("chatbot/", ChatBotFrontendController().intChatbot, name="chatbot.init"),

]
public_urls = [

]
api_urls: list[URLPattern] = [
    path("api/v2/chatbot/query/", ChatbotQueryApiController.as_view(), name="chatbot-query"),
]
urlpatterns += admin_auth_urls + admin_dashboard_urls + public_urls + api_urls
# Serve media files in development
if settings.DEBUG:
    urlpatterns += settings.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)