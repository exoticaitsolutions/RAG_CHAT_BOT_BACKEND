import logging
import random
import string
import tempfile
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


class ChatBotController:
    # Create Chat bot Api
    def create_chatbot_assistant(self, request):
        user_id = request.user.id
        logger.info(f"📩 Received request  user_id: {user_id}")
        openai_key = getattr(settings, "OPENAI_API_KEY", "")  # Use environment variables for security
        if not openai_key:
            messages.error(request, "Please fill your OpenAI API key first.")
        chatbots = ChatBotDB.objects.filter(user=user_id)
        data = {"user_chatbots": chatbots}
        context = {"chatbot": chatbots, "data": data}
        if request.method == "POST":
            user_agent_string = request.META.get('HTTP_USER_AGENT')
            ua = parse(user_agent_string)
            device = ua.device.family if ua.device.family else ""
            print('device', device)
            formdata = request.POST  # Form data
            chatbot_name = formdata.get('chatbotname')
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            udata = User.objects.get(id=user_id)
            chatbot_appearance = ChatbotAppearance.objects.create(chatbot_id=random_string, display_name=chatbot_name)
            ChatBotDB.objects.create(chatbot_name=chatbot_name, chatbot_id=random_string, user=udata,chatbot_appearance=chatbot_appearance)
            messages.success(request, 'Chatbot added successfully.')
        return render(request, 'admin/page/chatbot/CreateChatBotForm.html',context=context)
    
    
    def get_chatbot_assistant_by_chat_id(self, request,c_id):
        id = c_id
        user_id = request.user.id
        logger.info(f"📩 Received request  c_id: {c_id} and user id = {user_id}")
        data = ChatbotDetails(c_id,user_id)
        return render(request, 'admin/page/chatbot/Uploader/add_document_in_chatbot.html',locals())
    
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
    
    
    @csrf_exempt
    def RefreshDiv(self, request):
        c_id = request.GET.get('chat_id')
        u_id = request.GET.get('user_id')
        documents = Document.objects.filter(chatbot=c_id, user=u_id)
        print(f'documents == {documents}')
        return render(request, 'admin/Ajax/Chatbot/GetChatBotinfoAndRefreshContent.html', {'documents': documents})