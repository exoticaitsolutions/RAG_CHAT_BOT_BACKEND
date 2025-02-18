import logging
import random
import string
import tempfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q


from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework.views import csrf_exempt
from user_agents import parse
from RAG_CHATBOT_BACKEND_APIS.app.services.ChatbotService import ChatbotDetails
from RAG_CHATBOT_BACKEND_APIS.models import *

logger = logging.getLogger(__name__)


class ForgetPasswordController:
    # Create Chat bot Api
    
    # @method_decorator(login_required(login_url='/login/'))
    def forget_password_page(self, request):
        if request.method == "POST":
            email = request.POST.get("email")
            user = CustomUser.objects.filter(email=email).exists()
            if user:
                print(email, "---------")
            else:
                print("Your email is incorrect, please try again!!!")
                messages.error(request, "Your email is incorrect, please try again!!!")
                return redirect("/forget-password/")
        return render(request, 'admin/auth/forgetpasswordpage.html')
    #     user_id = request.user.id
    #     logger.info(f"📩 Received request  user_id: {user_id}")
    #     print(f"📩 Received request  user_id: {user_id}")
    #     openai_key = getattr(settings, "OPENAI_API_KEY", "")  # Use environment variables for security
    #     if not openai_key:
    #         messages.error(request, "Please fill your OpenAI API key first.")
    #     chatbots = ChatBotDB.objects.filter(user=user_id)
    #     data = {"user_chatbots": chatbots}
    #     context = {"chatbot": chatbots, "data": data}
    #     if request.method == "POST":
    #         user_agent_string = request.META.get('HTTP_USER_AGENT')
    #         ua = parse(user_agent_string)
    #         device = ua.device.family if ua.device.family else ""
    #         print('device', device)
    #         formdata = request.POST  # Form data
    #         chatbot_name = formdata.get('chatbotname')
    #         random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    #         udata = CustomUser.objects.get(id=user_id)
    #         chatbot_appearance = ChatbotAppearance.objects.create(chatbot_id=random_string, display_name=chatbot_name)
    #         ChatBotDB.objects.create(chatbot_name=chatbot_name,openai_key=openai_key , chatbot_id=random_string, user=udata,chatbot_appearance=chatbot_appearance)
    #         messages.success(request, 'Chatbot added successfully.')
    #     return render(request, 'admin/page/chatbot/CreateChatBotForm.html',context=context)
    
    # @method_decorator(login_required(login_url='/login/'))
    # def get_chatbot_assistant_by_chat_id(self, request,c_id):
    #     user_id = request.user.id
    #     logger.info(f"📩 Received request  c_id: {c_id} and user id = {user_id}")
    #     data = ChatbotDetails(c_id,user_id)
    #     return render(request, 'admin/page/chatbot/Uploader/add_document_in_chatbot.html',locals())
    
    
    # @method_decorator(login_required(login_url='/login/'), name='dispatch')
    # def render_the_webiste_url(self, request, c_id):
    #     user_id = request.user.id
    #     chatbot_data = ChatBotDB.objects.filter(Q(id=c_id) | Q(chatbot_id=c_id), user_id=user_id).first()  # Use `.first()` to avoid exceptions if no result is found
    #     data = ChatbotDetails(c_id,user_id)
    #     return render(request, 'admin/page/chatbot/Uploader/add-website-list.html', locals())

    # @method_decorator(login_required(login_url='/login/'))
    # def render_the_webiste_preview(self, request,c_id):
    #     user_id = request.user.id
    #     logger.info(f"📩 Received request  c_id: {c_id} and user id = {user_id}")
    #     data = ChatbotDetails(c_id,user_id)
    #     return render(request, 'admin/page/chatbot/pages/preview-chat-page.html')
    
    # @method_decorator(login_required(login_url='/login/'))
    # def render_website_share(self, request,c_id):
    #     user_id = request.user.id
    #     logger.info(f"📩 Received request  c_id: {c_id} and user id = {user_id}")
    #     data = ChatbotDetails(c_id,user_id)
    #     context = {'data': data }
    #     print('context',context)
    #     return render(request, 'admin/page/chatbot/Uploader/share_chat_bot.html',context=context)

    # @csrf_exempt
    # @method_decorator(login_required(login_url='/login/'))
    # def RefreshDiv(self, request):
    #     c_id = request.GET.get('chat_id')
    #     u_id = request.GET.get('user_id')
    #     documents = Document.objects.filter(chatbot=c_id) # type: ignore
    #     return render(request, 'admin/Ajax/Chatbot/GetChatBotinfoAndRefreshContent.html', {'documents': documents})
