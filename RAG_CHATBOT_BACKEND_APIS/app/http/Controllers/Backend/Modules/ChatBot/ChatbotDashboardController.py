import logging
import os
import socket
import threading
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.AuthProfileController import AuthServices
from RAG_CHATBOT_BACKEND_APIS.app.http.Serializers.Modules.Chatbot.ChatbotSerializer import DocumentUploadSerializer
from RAG_CHATBOT_BACKEND_APIS.app.services.Modules.Chatbot.ChatBotService import ChatBotService
from RAG_CHATBOT_BACKEND_APIS.app.services.Modules.Chatbot.chatbot_content_service import ChatbotContentManagementService
from RAG_CHATBOT_BACKEND_APIS.models import Chat, ChatBotDB, ChatHistory, DocumentNamespaceIds
from RAG_CHATBOT_BACKEND_APIS.utils import create_directories, format_name
from RAG_CHATBOT_BACKEND_APIS.views import ChatbotAppearance
import traceback

logger = logging.getLogger(__name__)

class ChatbotDashboardController:
    @method_decorator(login_required(login_url='/login/'))
    def view_chatbot_dashboard(self, request, user_uuid, chatbot_id, view_type):
        try:
            user_id = request.user.id
            chatbot_instance_id = ChatBotDB.objects.filter(chatbot_id=chatbot_id).values_list('id', flat=True).first()
            chatbot_data = ChatBotService.ChatbotDetails(chatbot_instance_id, user_id)  # type: ignore
            chats = Chat.objects.filter(user=request.user.id, chatbot_id=chatbot_instance_id)
            chat_history = ChatHistory.objects.filter(user=request.user.id, chatbot_id=chatbot_instance_id)
            cfg = ChatbotAppearance.objects.get(chatbot_id=chatbot_id)

            context = {
                "data": {
                    "user_chatbots": chatbot_data,
                    "chats": chats,
                    "chat_history": chat_history,
                    "cfg": cfg
                }
            }

            view_map = {
                'document-list': 'admin/Pages/ChatBot/admin_create_chatbot.html',
                'website-list': 'admin/Pages/ChatBot/add-website-list.html',
                'chat-page-preview': 'admin/Pages/ChatBot/ChatBotPreview.html',
                'chat-history': 'admin/Pages/ChatBot/chat_History.html',
                'settings-training': 'admin/Pages/ChatBot/ChatBotSetting/chat_setting.html',
                'settings-chatbot-appearance': 'admin/Pages/ChatBot/ChatBotSetting/chat_setting_apperence.html',
                'settings-chatbot-delete': 'admin/Pages/ChatBot/ChatBotSetting/delete_chatbot_data.html',
                'integration': 'admin/Pages/ChatBot/share_chat_bot.html',
            }

            if view_type in view_map:
                return render(request, view_map[view_type], context)
            else:
                logger.error("❌ Invalid view type!")
                return JsonResponse({"status": "error", "message": "Invalid view type"}, status=400)

        except Exception as e:
            logger.error(f"🚨 Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({"status": "error", "message": "An unexpected error occurred"}, status=500)

    @method_decorator(login_required(login_url='/login/'))
    def upload_and_start_training(self, request, user_uuid, chatbot_id, upload_type):
        if upload_type =='file':
            result = self._handle_training_logic_for_uploading_documents(request, user_uuid, chatbot_id)
            if result["status"] == "error":
                messages.error(request, result["message"])
                return JsonResponse(result, status=400)
            messages.success(request, "🎯 Documents uploaded and training started successfully! 🚀")
            return JsonResponse(result, status=200)
        else:
            logger.error("❌ Invalid view type!")
            return JsonResponse({"status": "error", "message": "Invalid view type"}, status=400)
            
    
    def _handle_training_logic_for_uploading_documents(self, request, user_uuid, chatbot_id):
        try:
            user_id = request.user.id
            chatbot = ChatBotService.get_chatbot_by_user_and_id(chatbot_id, user_id)

            if not chatbot:
                logger.error(f"🚫 Chatbot with ID {chatbot_id} not found for user {request.user.username}")
                return {"status": "error", "message": f"Chatbot with ID {chatbot_id} not found"}
            user = AuthServices.fetch_user_data('uuid', user_uuid)
            if not user:
                logger.error(f"🚷 User with UUID {user_uuid} not found!")
                return {"status": "error", "message": "User not found"}
            response , message , uploaded_documents = ChatbotContentManagementService.upload_and_process_chatbot_documents(user,chatbot,request.FILES)
            if not response:
                messages.error(request, message)
                logger.error(f"🌐 Network error occurred: {str(message)}")
                return JsonResponse({"status": "error", "message": message}, status=500)
            print(response,message)
            return {"status": "success", "uploaded_documents": uploaded_documents}
        except socket.error as e:
            logger.error(f"🌐 Network error occurred: {str(e)}")
            messages.error(request, "Network error! Please check your connection and try again.")
            return JsonResponse({"status": "error", "message": "Network error occurred"}, status=500)
        except Exception as e:
            logger.error(f"🚨 Unexpected error: {str(e)}")
            return {"status": "error", "message": "An unexpected error occurred"}
        
