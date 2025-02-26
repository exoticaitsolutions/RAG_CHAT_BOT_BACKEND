from django.urls import path

# Import Controllers
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.AdminDashboardController import AdminDashboardController
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.Auth.AuthController import AuthController
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.Auth.AuthProfileController import ProfileSettingController
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.Auth.ForgetPasswordController import ForgetPasswordController
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.Auth.ResetPasswordController import ResetPasswordController
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.Modules.ChatBot.ChatBotController import ChatBotController
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.Modules.ChatBot.ChatbotDashboardController import ChatbotDashboardController
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.ChatBotFrontendController import ChatBotFrontendController
from RAG_CHATBOT_BACKEND_APIS.app.Http.Middleware.auth_middleware import custom_login_required, redirect_if_authenticated

# Define URL patterns
urlpatterns = []

# Authentication URLs
admin_auth_urls = [
    path('register/', redirect_if_authenticated(AuthController().auth_register_page), name='register'),
    path('login/', redirect_if_authenticated(AuthController().auth_login_page), name='login'),
    path("forget-password/", redirect_if_authenticated(ForgetPasswordController().forget_password_page), name="forget-password"),
    path('reset-password/<uidb64>/<token>/', redirect_if_authenticated(ResetPasswordController().reset_password_page), name='reset_password'),
]

# Admin Dashboard URLs
admin_dashboard_urls = [
    # Dashboard URL
    # path("dashboard/", AdminDashboardController().admin_dashboard_page, name="admin.dashboard"),
    path('dashboard/', custom_login_required(AdminDashboardController().admin_dashboard_page), name='admin_dashboard'),
    
    # Profile Settings
    path('dashboard/profile/<str:user_uuid>/setting-account/', custom_login_required(ProfileSettingController().SettingProfileAccount), name='admin.profile.setting.profile'),
    path("dashboard/profile/<str:user_uuid>/setting-security/", custom_login_required(ProfileSettingController().SettingProfileSercurity), name="admin.profile.setting.security"),
    
    # User Chatbot Management
    path("dashboard/user/<str:user_uuid>/chatbot/", custom_login_required(ChatBotController().chatbot_dashboard_view), name="admin.user.chatbot"),
    path('dashboard/chatbot/fetch-modal-content/', custom_login_required(ChatBotController().fetch_modal_content), name='admin.fetch_modal_content_for_chat_bot'),
    path("dashboard/user/<str:user_uuid>/chatbot/<str:chatbot_id>/<str:view_type>/", custom_login_required(ChatbotDashboardController().view_chatbot_dashboard), name="admin.user.chatbot.dashboard"),

    # Upload Documents and Website Data  for Chatbot
    path("dashboard/user/<str:user_uuid>/chatbot/post/<str:curd_type>", custom_login_required(ChatBotController().handle_chatbot_action), name="admin.user.chatbot.manage"),
    path("dashboard/user/<str:user_uuid>/chatbot/<str:chatbot_id>/upload/<str:upload_type>", custom_login_required(ChatbotDashboardController().upload_and_start_training), name="admin.user.chatbot.upload-document"),
    

]

# Public URLs (if any, add them here)
public_urls = [
    # Chatbot Frontend
    path("chatbot/", ChatBotFrontendController().intChatbot, name="chatbot.init"),
]

# Combine all URL patterns
urlpatterns += admin_auth_urls + admin_dashboard_urls + public_urls 

# Serve media files in development mode

