from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from RAG_CHATBOT_BACKEND_APIS import admin_view
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.API.APIDocumentController import APIDocumentController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.API.ChromaQueryAPIViewController import ChromaQueryAPIViewController
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.ChatBot.ChatBotController import ChatBotController
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

# Grouped URL patterns
urlpatterns = [
  
]
# Admin Authentication
admin_auth_urls = [
    # Login Routes 
    path('login/', LoginController.as_view(), name='login.get'),
    # Register Routes
    path('register/', RegisterController.as_view(), name='register.get'),
]
# API Endpoints
api_urls = [
    path("api/v2/upload/pdf/", APIDocumentController.as_view(), name="upload_pdf"),
    # path("pdf/api/v1/upload-pdf/", views.upload_pdf_with_loader, name="upload_pdf_with_loader"),
    path("api/v2/query/", ChromaQueryAPIViewController.as_view(), name="chroma_query"),

]


# Admin Dashboard
admin_dashboard_urls = [
    # CHAT Bot Intergation
    path("dashboard/services/chatbot/create/", ChatBotController().create_chatbot_assistant, name="admin_dashborad_add_assistant_page"),
    path("dashboard/services/chatbot/get/<str:c_id>", ChatBotController().get_chatbot_assistant_by_chat_id, name="document-list"),
    path('upload-document/<str:c_id>', ChatBotController().upload_and_train, name="upload-document"), # type: ignore
    path("dashboard/services/chatbot/preview/<str:c_id>/", admin_view.admin_dashboard_preview_chat_bot, name="preview-chatbot"),
    
    
    path("dashboard/home/", admin_view.admin_dashborad_page, name="admin_dashborad_page"),
    path("dashboard/services/chatbot/create/", admin_view.admin_dashborad_add_assistant_page, name="admin_dashborad_add_assistant_page"),
    
    
    path("dashboard/services/chatbot/history/<str:c_id>/", admin_view.admin_dashborad_chatbot_history, name="chat-history"),
    path("dashboard/services/chatbot/setting/<str:c_id>/", admin_view.admin_dashborad_chatbot_setting, name="chat-setting"),
    path("dashboard/services/chatbot/chatbot-appearance/<str:c_id>/", admin_view.admin_dashborad_chatbot_setting_apperence, name="chat-setting-apperence"),
    path("dashboard/services/chatbot/delete/<str:c_id>/", admin_view.admin_dashborad_chatbot_delete, name="chat-setting-delete"),
    path("dashboard/services/chatbot/intergation/<str:c_id>/", admin_view.admin_dashborad_chatbot_share, name="chat-setting-intergation"),

    path('dashboard/services/chatbot/website-list/', admin_view.website_list, name='website-list'),
    
    path('chatbot/', admin_view.chatbot_view, name='chatbot'),
    


]

# Chatbot Services
chatbot_urls = [
   #  path("chatbot/chatbot-history/<str:c_id>/", admin_view.admin_dashborad_chatbot_history, name="chat-history"),
]


# Swagger Documentation
swagger_urls = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

# Combine all routes
urlpatterns += admin_auth_urls + admin_dashboard_urls + chatbot_urls + api_urls + swagger_urls

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
