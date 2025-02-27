from django.urls import path
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.API.Chatbot.ChatbotAppearanceController import ChatbotAppearanceController
from RAG_CHATBOT_BACKEND_APIS.app.Http.Controllers.Backend.API.Chatbot.ChatbotQueryApiController import ChatbotQueryApiController

urlpatterns = [
     path("chatbot/appearances/", ChatbotAppearanceController.as_view(), name="chatbot-query"),
    path("chatbot/query/", ChatbotQueryApiController.as_view(), name="chatbot-query"),
]