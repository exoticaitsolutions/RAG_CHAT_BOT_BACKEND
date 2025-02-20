import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from RAG_CHATBOT_BACKEND_APIS.app.services.Modules.Chatbot.ChatBotService import ChatBotService
from RAG_CHATBOT_BACKEND_APIS.views import JsonResponse
logger = logging.getLogger(__name__)

class ChatBotController:
    # Create A Chat BOT Page
    @method_decorator(login_required(login_url='/login/'))
    def chatbot_dashboard_view(self, request, user_uuid):
        user = request.user
        logger.info(f"Rendering chatbot dashboard for user: {user_uuid}")
        openai_key = getattr(settings, "OPENAI_API_KEY", "")
        if not openai_key:
            messages.error(request, "Please fill your OpenAI API key first.")
        chatbots = ChatBotService.get_user_chatbots(user.id)
        # Pass destination in context
        context = {"chatbot": chatbots, "data": {"user_chatbots": chatbots}}
        return render(request, 'admin/page/chatbot/CreateChatBotForm.html', context)
    
    @method_decorator(login_required(login_url='/login/'))
    @csrf_exempt  # Disable CSRF protection
    def fetch_modal_content(self, request):
        logger.info("Fetching modal content.")
        user_id = request.POST.get('user_id')
        chat_type = request.POST.get('chat_type')
        chat_id = request.POST.get('chat_id')
        if chat_type == 'create':
            data ={}
            header,button_name ="Add Chat Bot","Create"
        else:   
            data = ChatBotService.get_chatbot_by_id(chat_id)
            header,button_name ="Update Chat Bot","Update"
        context = {"chat_type": chat_type ,"user_id":user_id, "data":data ,"header": header ,"button_name":button_name}
        html_content = render(request, 'admin/Ajax/Chatbot/dynamic_chatbot_modal_content.html', context).content.decode('utf-8')
        return JsonResponse({"status": "success", "message": "rendore the html successfully" ,"html" : html_content}, status=200)


    @method_decorator(login_required(login_url='/login/'))
    def handle_chatbot_action(self, request, user_uuid, curd_type):
        formdata = request.POST
        chatbot_name = formdata.get('chatbotname')
        chat_id = formdata.get('chat_id')
        user = request.user
        if curd_type == 'create':
            response = ChatBotService.create_chatbot(user, chatbot_name)
        elif curd_type == 'edit':
            response = ChatBotService.update_chatbot(user, chatbot_name, chat_id)
        elif curd_type == 'delete':
            response = ChatBotService.delete_chatbot(chat_id)
        else:
            response = {"error": "Invalid action."}
        if "success" in response:
            messages.success(request, response["success"])
        else:
            messages.error(request, response["error"])
        return render(request, 'admin/page/chatbot/CreateChatBotForm.html')
