import logging
import os
import random
import string
from RAG_Backend import settings
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, ChatbotAppearance
from RAG_CHATBOT_BACKEND_APIS.utils import copy_directory_contents, delete_folder, format_name

logger = logging.getLogger(__name__)

class ChatBotService:

    @staticmethod
    def get_user_chatbots(user_id):
        """Fetch all chatbots for a given user."""
        try:
            return ChatBotDB.objects.filter(user=user_id).only("chatbot_name")
        except Exception as e:
            logger.error(f"Error fetching chatbots for user {user_id}: {e}")
            return []

    @staticmethod
    def get_chatbot_by_id(chatbot_id):
        """Fetch a single chatbot by ID."""
        try:
            return ChatBotDB.objects.filter(chatbot_id=chatbot_id).first()
        except Exception as e:
            logger.error(f"Error fetching chatbot ID {chatbot_id}: {e}")
            return None
    @staticmethod
    def generate_chatbot_id():
        """Generates a random 15-character chatbot ID."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

    @staticmethod
    def create_chatbot(user, chatbot_name):
        """Handles chatbot creation logic."""
        user_slug = format_name(user.username)
        chatbot_slug = format_name(chatbot_name)
        chatbot_id = ChatBotService.generate_chatbot_id()
        
        chat_bot_media_path = os.path.join(settings.MEDIA_ROOT, user_slug, chatbot_slug)
        upload_path = os.path.join(chat_bot_media_path, "upload")
        chroma_db_path = os.path.join(chat_bot_media_path, "chroma_db")

        # Check if chatbot already exists
        if ChatBotDB.objects.filter(user=user, chatbot_name=chatbot_name).exists():
            return {"error": "Chatbot with this name already exists."}
        try:
            os.makedirs(upload_path, exist_ok=True)
            os.makedirs(chroma_db_path, exist_ok=True)
            copy_directory_contents(settings.COPY_ROOT, chat_bot_media_path)
        except Exception as e:
            logger.error(f"❌ Error creating chatbot directories: {e}")
            return {"error": "Failed to create chatbot directories."}

        chat_bot_media_url = f"{settings.MEDIA_URL}{user_slug}/{chatbot_slug}/"
        icon_url = f"{chat_bot_media_url}default_images/chatbot_image.png"
        chatbot_launcher_icon = f"{chat_bot_media_url}default_images/avatar-1.png"
        chatbot_background_pattern = f"{chat_bot_media_url}chatbot_background_patterns/0fac5419_pattern_9.jpg"

        chatbot_appearance = ChatbotAppearance.objects.create(
            chatbot_id=chatbot_id,
            display_name=chatbot_name,
            chatbot_background_pattern=chatbot_background_pattern,
            chatbot_image=icon_url,
            chatbot_launcher_icon=chatbot_launcher_icon
        )

        ChatBotDB.objects.create(
            chatbot_name=chatbot_name,
            chatbot_id=chatbot_id,
            openai_key=getattr(settings, "OPENAI_API_KEY", ""),
            destination=f"{chat_bot_media_url}default_images/",
            icon_url=icon_url,
            chat_bot_media_url=chat_bot_media_url,
            chat_bot_media_path=chat_bot_media_path,
            user=user,
            chatbot_appearance=chatbot_appearance
        )

        return {"success": "Chatbot added successfully."}

    @staticmethod
    def update_chatbot(user, chatbot_name, chat_id):
        """Handles chatbot updating logic."""
        chatbot_data = ChatBotDB.objects.filter(chatbot_id=chat_id).first()
        if not chatbot_data:
            return {"error": "Chatbot not found."}

        old_chat_bot_media_path = chatbot_data.chat_bot_media_path

        try:
            delete_folder(old_chat_bot_media_path)
        except Exception as e:
            logger.error(f"❌ Error deleting old chatbot directory: {e}")
            return {"error": "Failed to delete old chatbot directory."}

        user_slug = format_name(user.username)
        chatbot_slug = format_name(chatbot_name)
        chat_bot_media_path = os.path.join(settings.MEDIA_ROOT, user_slug, chatbot_slug)

        try:
            os.makedirs(os.path.join(chat_bot_media_path, "upload"), exist_ok=True)
            os.makedirs(os.path.join(chat_bot_media_path, "chroma_db"), exist_ok=True)
            copy_directory_contents(settings.COPY_ROOT, chat_bot_media_path)
        except Exception as e:
            logger.error(f"❌ Error creating new chatbot directories: {e}")
            return {"error": "Failed to create new chatbot directories."}

        chat_bot_media_url = f"{settings.MEDIA_URL}{user_slug}/{chatbot_slug}/"
        icon_url = f"{chat_bot_media_url}default_images/chatbot_image.png"
        chatbot_background_pattern = f"{chat_bot_media_url}chatbot_background_patterns/0fac5419_pattern_9.jpg"

        chatbot_data.chatbot_name = chatbot_name
        chatbot_data.icon_url = icon_url # type: ignore
        chatbot_data.chat_bot_media_url = chat_bot_media_url
        chatbot_data.chat_bot_media_path = chat_bot_media_path
        chatbot_data.save()

        chatbot_appearance = ChatbotAppearance.objects.filter(id=chatbot_data.chatbot_appearance.id).first()
        if chatbot_appearance:
            chatbot_appearance.display_name = chatbot_name
            chatbot_appearance.chatbot_background_pattern = chatbot_background_pattern # type: ignore
            chatbot_appearance.chatbot_image = icon_url # type: ignore
            chatbot_appearance.save()
        else:
            return {"error": "Something went wrong with chatbot appearance data."}

        return {"success": "Chatbot successfully updated."}

    @staticmethod
    def delete_chatbot(chat_id):
        """Handles chatbot deletion."""
        chatbot_data = ChatBotDB.objects.filter(chatbot_id=chat_id).first()
        if not chatbot_data:
            return {"error": "Chatbot not found."}

        chat_bot_media_path = chatbot_data.chat_bot_media_path
        chatbot_data.chatbot_appearance.delete()
        chatbot_data.delete()

        try:
            delete_folder(chat_bot_media_path)
        except Exception as e:
            logger.error(f"❌ Error deleting chatbot folder: {e}")
            return {"error": "Failed to delete chatbot folder."}

        return {"success": "Chatbot successfully deleted."}
