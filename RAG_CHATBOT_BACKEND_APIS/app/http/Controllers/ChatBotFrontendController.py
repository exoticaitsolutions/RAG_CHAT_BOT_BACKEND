
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
logger = logging.getLogger(__name__)


class ChatBotFrontendController:
        def intChatbot(self, request):
            return render(request, "chatbot.html")
