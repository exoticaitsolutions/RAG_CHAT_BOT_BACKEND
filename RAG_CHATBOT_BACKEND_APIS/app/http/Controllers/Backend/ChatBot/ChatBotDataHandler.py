import logging
import random
import string
import tempfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework.views import csrf_exempt
from user_agents import parse
from RAG_Backend.settings import BASE_API_URL
from RAG_CHATBOT_BACKEND_APIS.app.services.ChatbotService import ChatbotDetails
from RAG_CHATBOT_BACKEND_APIS.models import *

logger = logging.getLogger(__name__)


class ChatBotDataHandler:
    # Uplaod the Documents COntroller 
    # Create Chat bot Api
    def upload_and_train(self, request, c_id):
        """ Upload document and train chatbot """
        user_id = request.user.id
        print('user_id',user_id)
        chat_id = c_id
        
        url = f"{BASE_API_URL}/api/v2/upload/?chat_id={chat_id}&user_id={user_id}"
        if request.method == 'POST' and request.FILES:
            files = []
            temp_dir = tempfile.gettempdir()
            for file_key in request.FILES:
                uploaded_file = request.FILES[file_key]
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, 'wb') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
                files.append(('file', (uploaded_file.name, open(file_path, 'rb'), uploaded_file.content_type)))
            try:
                response = requests.post(url, files=files)
                response_json = response.json() if response.status_code == 200 else None
                if response.status_code == 200:
                    messages.success(request, 'Files uploaded and training started.')
                    return JsonResponse({"status": "success", "message": "Files uploaded and training started", "response": response_json}, status=200)
                else:
                    messages.success(request, 'Files uploaded and training started.')
                    return JsonResponse({"status": "failed", "message": "Unexpected error", "response": response_json}, status=response.status_code)
            except requests.exceptions.RequestException as e:
                return JsonResponse({"status": "failed", "message": "Error making request", "error_details": str(e)}, status=500)
        return JsonResponse({"status": "failed", "message": "No files uploaded"}, status=400)
    
    