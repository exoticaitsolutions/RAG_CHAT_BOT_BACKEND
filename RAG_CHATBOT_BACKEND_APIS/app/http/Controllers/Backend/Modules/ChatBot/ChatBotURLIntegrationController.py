import logging
import random
import string
import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework.views import APIView, csrf_exempt
from user_agents import parse
from RAG_Backend.settings import BASE_API_URL
from RAG_CHATBOT_BACKEND_APIS.app.services.ChatbotService import ChatbotDetails
from RAG_CHATBOT_BACKEND_APIS.models import *
logger = logging.getLogger(__name__)

class ChatBotURLIntegrationController(APIView):
    # Create Chat bot Api
    def render_the_webiste_url(self, request):
        return render(request, 'admin/page/chatbot/Uploader/add-website-list.html')
