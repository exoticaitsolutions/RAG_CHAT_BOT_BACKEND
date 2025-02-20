from django.urls import path, re_path

from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.AdminDashboardController import AdminDashboardController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.AuthController import AuthController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.AuthProfileController import ProfileSettingController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.ForgetPasswordController import ForgetPasswordController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.ResetPasswordController import ResetPasswordController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Modules.ChatBot.ChatBotController import ChatBotController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Modules.ChatBot.ChatbotDashboardController import ChatbotDashboardController


<<<<<<< HEAD

from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.ChatBot.ChatBotDataHandler import ChatBotDataHandler
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.ChatBot.ChatBotURLIntegrationController import ChatBotURLIntegrationController
from . import views
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.RegisterController import RegisterController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.LoginController import LoginController

# Define schema view for Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="File Upload API",
        default_version="v1",
        description="API for uploading PDFs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)
=======
>>>>>>> d1b87efc5be916f959b1b61e0ae8fa5160a2637e

# ======================================
#               URL Patterns
# ======================================

# Core URLs
urlpatterns = [
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path("chatbot/appearance/", views.chatbot_appearance_form_view, name="chatbot-appearance-save"),
    # API Endpoints
    path("api/v1/upload/pdf/", APIDocumentController.as_view(), name="upload_pdf"),
    path("api/v1/query/", ChromaQueryAPIViewController.as_view(), name="chroma_query"),
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    
]
# Admin Authentication
admin_auth_urls = [
    path('register/', AuthController().auth_register_page, name='register'),
    path('login/', AuthController().auth_login_page, name='login'),
    # Forget Password page 
    # Forget Password
    path("forget-password/", ForgetPasswordController().forget_password_page, name="forget-password"),
    
    # Reset Password
    path('reset-password/<uidb64>/<token>/', ResetPasswordController().reset_password_page,  name='reset_password'),
]


# Admin Dashboard
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
]
public_urls = [

]
api_urls = [

]
urlpatterns += admin_auth_urls + admin_dashboard_urls + public_urls + api_urls
# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
