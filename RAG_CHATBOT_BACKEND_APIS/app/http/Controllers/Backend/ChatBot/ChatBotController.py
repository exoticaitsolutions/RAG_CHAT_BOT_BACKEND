import logging
import os
import random
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, ChatbotAppearance
from RAG_CHATBOT_BACKEND_APIS.utils import copy_directory_contents, format_name

logger = logging.getLogger(__name__)

class ChatBotController:
    @method_decorator(login_required(login_url='/login/'))
    def create_chatbot_assistant(self, request, user_uuid):
        user = request.user
        logger.info(f"📩 Received request user_id: {user.id}")

        # Validate OpenAI Key
        openai_key = getattr(settings, "OPENAI_API_KEY", "")
        if not openai_key:
            messages.error(request, "Please fill your OpenAI API key first.")
            return redirect(f"/dashboard/user/{user_uuid}/chatbot/create/")

        chatbots = ChatBotDB.objects.filter(user=user.id).only("chatbot_name")
        
        # Define destination before any condition
        destination = ""

        if request.method == "POST":
            formdata = request.POST
            chatbot_name = formdata.get('chatbotname')

            if not chatbot_name:
                messages.error(request, "Chatbot name is required.")
                return redirect(f"/dashboard/user/{user_uuid}/chatbot/create/")

            chatbot_slug = format_name(chatbot_name)
            user_slug = format_name(user.username)
            destination = os.path.join(settings.MEDIA_ROOT, user_slug, chatbot_slug)
            upload_path = os.path.join(destination, "upload")
            chroma_db_path = os.path.join(destination, "chroma_db")

            # Prevent duplicate chatbot names
            if ChatBotDB.objects.filter(user=user, chatbot_name=chatbot_name).exists():
                messages.error(request, "Chatbot with this name already exists.")
                return redirect(f"/dashboard/user/{user_uuid}/chatbot/create/")

            try:
                os.makedirs(upload_path, exist_ok=True)
                os.makedirs(chroma_db_path, exist_ok=True)
                copy_directory_contents(settings.COPY_ROOT, destination)
            except Exception as e:
                logger.error(f"❌ Error creating chatbot directories: {e}")
                messages.error(request, "Failed to create chatbot directories.")
                return redirect(f"/dashboard/user/{user_uuid}/chatbot/create/")
            destination = request.build_absolute_uri(
                f"{settings.MEDIA_URL}{user_slug}/{chatbot_slug}/default_images/"
            )
            icon_url = request.build_absolute_uri(
                f"{settings.MEDIA_URL}{user_slug}/{chatbot_slug}/default_images/chatbot_image.png"
            )

            chatbot_launcher_icon = request.build_absolute_uri(
                f"{settings.MEDIA_URL}{user_slug}/{chatbot_slug}/default_images/avatar-1.png"
            )

            chatbot_background_pattern = request.build_absolute_uri(
                f"{settings.MEDIA_URL}{user_slug}/{chatbot_slug}/chatbot_background_patterns/0fac5419_pattern_9.jpg"
            )

            chatbot_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            
            chatbot_appearance = ChatbotAppearance.objects.create(
                chatbot_id=chatbot_id, display_name=chatbot_name,
                chatbot_background_pattern= chatbot_background_pattern,
                chatbot_image=icon_url,
                chatbot_launcher_icon=chatbot_launcher_icon
            )
            ChatBotDB.objects.create(
                chatbot_name=chatbot_name,
                openai_key=openai_key,
                chatbot_id=chatbot_id,
                destination=destination,
                icon_url =icon_url,
                user=user,
                chatbot_appearance=chatbot_appearance
            )

            messages.success(request, 'Chatbot added successfully.')
            return redirect(f"/dashboard/user/{user_uuid}/chatbot/create/")

        # Pass destination in context
        context = {"chatbot": chatbots, "data": {"user_chatbots": chatbots}, "destination": destination}
        return render(request, 'admin/page/chatbot/CreateChatBotForm.html', context)
