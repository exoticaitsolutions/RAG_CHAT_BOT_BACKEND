import logging
import socket
import traceback
from urllib.parse import urlparse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from RAG_CHATBOT_BACKEND_APIS.app.http.Controllers.Backend.Auth.AuthController import AuthServices
from RAG_CHATBOT_BACKEND_APIS.app.services.Modules.Chatbot.ChatBotService import ChatBotService
from RAG_CHATBOT_BACKEND_APIS.app.services.Modules.Chatbot.chatbot_content_service import ChatbotContentManagementService
from RAG_CHATBOT_BACKEND_APIS.models import Chat, ChatBotDB, ChatHistory, ChatbotAppearance, Document, WebsiteDB
# Configure logger
logger = logging.getLogger(__name__)

class ChatbotDashboardController:
    """
    Controller for handling chatbot dashboard functionalities, including viewing chatbot details, 
    uploading training documents, and handling website URL uploads.
    """

    @method_decorator(login_required(login_url='/login/'))
    def view_chatbot_dashboard(self, request, user_uuid, chatbot_id, view_type):
        """
        Renders the chatbot dashboard based on the provided view type.
        Retrieves chatbot details, chat history, and associated documents/websites.
        """
        try:
            user_id = request.user.id
            chatbot_instance = ChatBotDB.objects.filter(chatbot_id=chatbot_id).first()
            if not chatbot_instance:
                logger.error(f"🚫 Chatbot with ID {chatbot_id} not found!")
                return JsonResponse({"status": "error", "message": "Chatbot not found"}, status=404)

            chatbot_data = ChatBotService.ChatbotDetails(chatbot_instance.id, user_id) # type: ignore
            chats = Chat.objects.filter(user=user_id, chatbot_id=chatbot_instance.id)  # type: ignore
            chat_history = ChatHistory.objects.filter(user=user_id, chatbot_id=chatbot_instance.id) # type: ignore
            cfg = ChatbotAppearance.objects.filter(chatbot_id=chatbot_id).first()
            documents = Document.objects.filter(chatbot=chatbot_instance, user=user_id)
            websites = WebsiteDB.objects.filter(chatbot=chatbot_instance, user=user_id)

            context = {
                "data": {
                    "user_chatbots": chatbot_data,
                    "chats": chats,
                    "chat_history": chat_history,
                    "cfg": cfg,
                    "documents_data": {"documents": documents, "doc_count": documents.count()},
                    "websites_data": {"websites": websites, "web_count": websites.count()},
                }
            }
            logger.info("✅ Dashboard data prepared successfully.")

            # Mapping view types to respective template pages
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

            return render(request, view_map.get(view_type, 'error_page.html'), context)
        except Exception as e:
            logger.error(f"🚨 Unexpected error: {str(e)}\n{traceback.format_exc()}")
            return JsonResponse({"status": "error", "message": "An unexpected error occurred"}, status=500)

    @method_decorator(login_required(login_url='/login/'))
    def upload_and_start_training(self, request, user_uuid, chatbot_id, upload_type):
        """
        Handles the upload process for chatbot training data.
        Supports both document file uploads and website URL submissions.
        """
        try:
            if upload_type == 'file':
                result = self._handle_training_logic_for_uploading_documents(request, user_uuid, chatbot_id)
            elif upload_type == 'upload-website':
                result = self._handle_training_logic_for_website_urls(request, user_uuid, chatbot_id)
            else:
                logger.error("❌ Invalid upload type!")
                return JsonResponse({"status": "error", "message": "Invalid upload type"}, status=400)
            
            if result["status"] == "error":
                messages.error(request, result["message"])
                return JsonResponse(result, status=400)
            
            messages.success(request, "✅ Training started successfully! 🚀")
            return redirect(f"/dashboard/user/{user_uuid}/chatbot/{chatbot_id}/website-list/")
        except Exception as e:
            logger.error(f"🚨 Unexpected error: {str(e)}\n{traceback.format_exc()}")
            return JsonResponse({"status": "error", "message": "An unexpected error occurred"}, status=500)

    def _handle_training_logic_for_website_urls(self, request, user_uuid, chatbot_id):
        """
        Processes and validates website URL uploads for chatbot training.
        """
        try:
            website_url = request.POST.get('url')
            if not website_url or not urlparse(website_url).scheme or not urlparse(website_url).netloc:
                logger.error("❌ Invalid or empty URL!")
                return {"status": "error", "message": "Invalid URL format"}

            user_id = request.user.id
            chatbot = ChatBotService.get_chatbot_by_user_and_id(chatbot_id, user_id)
            if not chatbot:
                return {"status": "error", "message": "Chatbot not found"}
            
            user = AuthServices.fetch_user_data('uuid', user_uuid)
            if not user:
                return {"status": "error", "message": "User not found"}
            
            response, message, uploaded_documents = ChatbotContentManagementService.upload_and_process_chatbot_website_urls(user, chatbot, website_url)
            return {"status": "success", "uploaded_documents": uploaded_documents}
        except Exception as e:
            logger.error(f"🚨 Error processing website URLs: {str(e)}")
            return {"status": "error", "message": "An error occurred"}

    def _handle_training_logic_for_uploading_documents(self, request, user_uuid, chatbot_id):
        """
        Processes document uploads for chatbot training.
        """
        try:
            user_id = request.user.id
            chatbot = ChatBotService.get_chatbot_by_user_and_id(chatbot_id, user_id)
            if not chatbot:
                return {"status": "error", "message": "Chatbot not found"}
            
            user = AuthServices.fetch_user_data('uuid', user_uuid)
            if not user:
                return {"status": "error", "message": "User not found"}
            
            response, message, uploaded_documents = ChatbotContentManagementService.upload_and_process_chatbot_documents(user, chatbot, request.FILES)
            return {"status": "success", "uploaded_documents": uploaded_documents}
        except Exception as e:
            logger.error(f"🚨 Error processing documents: {str(e)}")
            return {"status": "error", "message": "An error occurred"}
