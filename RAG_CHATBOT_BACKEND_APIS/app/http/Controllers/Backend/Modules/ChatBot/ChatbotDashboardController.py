import logging
from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from RAG_CHATBOT_BACKEND_APIS.app.services.Chatbot.ChatBotService import ChatBotService
from RAG_CHATBOT_BACKEND_APIS.app.services.ChatbotService import ChatbotDetails
from RAG_CHATBOT_BACKEND_APIS.models import Chat, ChatBotDB, ChatHistory
from RAG_CHATBOT_BACKEND_APIS.views import ChatbotAppearance

logger = logging.getLogger(__name__)


class ChatbotDashboardController:
    @method_decorator(login_required(login_url='/login/'))
    def view_chatbot_dashboard(self, request, user_uuid, chatbot_id, view_type):
        user_id = request.user.id
        chatbot_instance_id = ChatBotDB.objects.filter(chatbot_id=chatbot_id).values_list('id', flat=True).first()
        chatbot_data = ChatbotDetails(chatbot_instance_id, user_id) # type: ignore
        chats = Chat.objects.filter(user=request.user.id, chatbot_id=chatbot_instance_id)
        chat_history = ChatHistory.objects.filter(user=request.user.id, chatbot_id=chatbot_instance_id)
        cfg = ChatbotAppearance.objects.get(chatbot_id=chatbot_id)
        context = {"data": {"user_chatbots": chatbot_data,"chats": chats,"chat_history": chat_history, "cfg": cfg ,}}
        if view_type == 'document-list':
            return render(request, 'admin/Pages/ChatBot/admin_create_chatbot.html', context)
        elif view_type == 'website-list':
            return render(request, 'admin/Pages/ChatBot/add-website-list.html', context)
        elif view_type == 'chat-page-preview':
            return render(request, 'admin/Pages/ChatBot/ChatBotPreview.html', context)
        elif view_type == 'chat-history':
            return render(request, 'admin/Pages/ChatBot/chat_History.html', context)
        elif view_type == 'settings-training':
            return render(request, 'admin/Pages/ChatBot/ChatBotSetting/chat_setting.html', context)
        elif view_type == 'settings-chatbot-appearance':
            return render(request, 'admin/Pages/ChatBot/ChatBotSetting/chat_setting_apperence.html', context)
        elif view_type == 'settings-chatbot-delete':
            return render(request, 'admin/Pages/ChatBot/ChatBotSetting/delete_chatbot_data.html', context)
        elif view_type == 'integration':
            return render(request, 'admin/Pages/ChatBot/share_chat_bot.html', context)
        else:
            return JsonResponse({"error": "Invalid view type"}, status=400)
