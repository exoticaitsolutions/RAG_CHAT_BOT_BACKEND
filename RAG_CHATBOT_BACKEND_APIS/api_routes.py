from django.urls import path
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.API.Chatbot.ChatbotQueryApiController import ChatbotQueryApiController

urlpatterns = [
    path("chatbot/query/", ChatbotQueryApiController.as_view(), name="chatbot-query"),
]