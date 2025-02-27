
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render

from RAG_CHATBOT_BACKEND_APIS.utils import get_base_url
logger = logging.getLogger(__name__)


class ChatBotFrontendController:
        def intChatbot(self, request):
            base_url = get_base_url(request)
            context = { "base_url": base_url }
            return render(request, "chatbot.html",context)
        
        def Share_Links(self, request,cc_id):
            return render(request, "chatbot.html")
