from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
# from RAG_CHATBOT_BACKEND_APIS.views import chatbot_appearance_view
# from app.http.Controllers.chatbot_appearance_controller import chatbot_appearance_form_view
from RAG_CHATBOT_BACKEND_APIS.views import chatbot_appearance_form_view
# Import Controllers
from RAG_CHATBOT_BACKEND_APIS import admin_view
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.API.APIDocumentController import APIDocumentController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.API.ChromaQueryAPIViewController import ChromaQueryAPIViewController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.ChatBot.DocumentController import DocumentController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.RegisterController import RegisterController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.LoginController import LoginController
from . import views

# Swagger API Documentation Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="File Upload API",
        default_version="v1",
        description="API for uploading PDFs and querying ChromaDB",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# ======================================
#               URL Patterns
# ======================================

             

# Core URLs
urlpatterns = [
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path("chatbot/appearance/", chatbot_appearance_form_view, name="chatbot-appearance-save"),

    # path('chatbot-appearance-save/<str:chatbot_id>/', chatbot_appearance_save_view, name='chatbot-appearance-save'),
    # API Endpoints
    path("api/v1/upload/pdf/", APIDocumentController.as_view(), name="upload_pdf"),
    path("api/v1/query/", ChromaQueryAPIViewController.as_view(), name="chroma_query"),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    
]

# Admin Authentication URLs
admin_auth_urls = [
    path('login/', LoginController.as_view(), name='login.get'),
    path('register/', RegisterController.as_view(), name='register'),
]

# Admin Dashboard URLs
admin_dashboard_urls = [
    path("dashboard/services/chatbot/get/<str:c_id>/", DocumentController().show_upload_form, name="document-list"),
    # path("upload-document/<str:c_id>/", DocumentController().upload_and_train, name="upload-document"),
    path('upload-document/<str:c_id>', DocumentController().upload_and_train, name="upload-document"),
    path("dashboard/home/", admin_view.admin_dashborad_page, name="admin_dashborad_page"),
    path("dashboard/services/chatbot/create/", admin_view.admin_dashborad_add_assistant_page, name="admin_dashborad_add_assistant_page"),
    path("dashboard/services/chatbot/get1/<str:c_id>/", admin_view.admin_dashborad_document_list, name="document-list"),
    path("dashboard/services/chatbot/preview/<str:c_id>/", admin_view.admin_dashboard_preview_chat_bot, name="preview-chatbot"),
    path("dashboard/services/chatbot/history/<str:c_id>/", admin_view.admin_dashborad_chatbot_history, name="chat-history"),
    path("dashboard/services/chatbot/setting/<str:c_id>/", admin_view.admin_dashborad_chatbot_setting, name="chat-setting"),
    path("dashboard/services/chatbot/chatbot-appearance/<str:c_id>/", admin_view.admin_dashborad_chatbot_setting_apperence, name="chat-setting-apperence"),
    path("dashboard/services/chatbot/delete/<str:c_id>/", admin_view.admin_dashborad_chatbot_delete, name="chat-setting-delete"),

    path("dashboard/services/chatbot/intergation/<str:c_id>/", admin_view.admin_dashborad_chatbot_share, name="chat-setting-intergation"),
]

# Chatbot Services URLs
chatbot_urls = [
    # Placeholder for additional chatbot-related URLs
]

# Swagger API Documentation URLs
swagger_urls = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

# ======================================
#     Combine All Route Groups
# ======================================

urlpatterns += admin_auth_urls + admin_dashboard_urls + chatbot_urls + swagger_urls

# Serve Media Files in Development Mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
