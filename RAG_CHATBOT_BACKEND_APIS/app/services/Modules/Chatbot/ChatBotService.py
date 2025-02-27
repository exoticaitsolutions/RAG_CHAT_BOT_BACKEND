import logging
import os
import random
import string

from rest_framework.fields import ObjectDoesNotExist
from RAG_Backend import settings
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, ChatbotAppearance, CustomUser
from RAG_CHATBOT_BACKEND_APIS.utils import copy_directory_contents, create_directories, delete_folder, format_name

logger = logging.getLogger(__name__)

class ChatBotService:

    @staticmethod
    def int_code_generate(c_id: str, base_url: str):
        return {
            "chatbot_code" :f'<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script><script src="{base_url}static/chat-widget/chat-loader.js" chatbot-id="{c_id}" base_url="{base_url}" type="application/javascript"></script>',
            "chatbot_share_link": f'{base_url}share-public/{c_id}'
        }
    @staticmethod
    def ChatbotDetails(c_id: int, user_id: int):
        """
        Fetches chatbot details based on chatbot ID (c_id) and user ID (user_id).
        Returns a dictionary with chatbot data or None if not found.
        """
        try:
            CustomUserdata = CustomUser.objects.get(id=user_id)
            chatbot_data = ChatBotDB.objects.get(id=c_id, user_id=user_id)
            chatbot_count = ChatBotDB.objects.filter(user_id=user_id).count()
            user_chatbots = list(ChatBotDB.objects.filter(user_id=user_id))  # Convert QuerySet to list for safety
            # Constructing the response dictionary
            data = {
                "user_chatbots": user_chatbots,
                "chatbot": chatbot_data,
                "chatbot_count": chatbot_count,
                "chatbot_id": chatbot_data.id, # type: ignore
                "CustomUserdata_uuld" : CustomUserdata.uuid,
                "chat_bot_id": chatbot_data.chatbot_id,
                "chatbot_name": chatbot_data.chatbot_name,
                "llm_model": chatbot_data.llm_model,
                "model": chatbot_data.model,
                "temperature": chatbot_data.temperature,
                "context": chatbot_data.context,
                "openai_key": chatbot_data.openai_key,
                "vector_database": chatbot_data.vector_database,
                "pinecone_key": chatbot_data.pinecone_key,
                "pinecone_env": chatbot_data.pinecone_env,
                "visibility": chatbot_data.visibility,
                "hits": chatbot_data.hits,
                "seconds": chatbot_data.seconds,
                "pinecone_user_index": chatbot_data.pinecone_user_index,
            }
            return data
        except ObjectDoesNotExist:
            return None  # Returns None if no chatbot is found for the given user
        
    @staticmethod
    def get_chatbot_by_user_and_id(chat_id, user_id):
        try:
            chatbot = ChatBotDB.objects.get(chatbot_id=chat_id, user_id=user_id)
            return chatbot
        except ChatBotDB.DoesNotExist:
            return None
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
    def chat_bot_folder_strucuture(user_data , chat_bot_name):
        smedia_file, media_bot_ = create_directories(str(user_data.username), str(chat_bot_name))
        copy_path = os.path.join(settings.COPY_ROOT, 'chat_bot')
        try:
            copy_directory_contents(copy_path, smedia_file)
            return [True, smedia_file, media_bot_]
        except Exception as e:
            logger.error(f"❌ Error creating new chatbot directories: {e}")
            return [False,'' , '']
    @staticmethod
    def create_chatbot(user, chatbot_name):
        chatbot_id = ChatBotService.generate_chatbot_id()
        if ChatBotDB.objects.filter(user=user, chatbot_name=chatbot_name).exists():
            return {"error": "Chatbot with this name already exists."}
        response = ChatBotService.chat_bot_folder_strucuture(user,chatbot_name)
        """Handles chatbot creation logic."""
        if not  response[0]:
            return {"error": "Something Wrong."}
        chat_bot_media_url = f"{format_name(user.username)}/uploads/{format_name(chatbot_name)}/"
        chat_bot_user_chroma_path = f"{settings.MEDIA_URL}{format_name(user.username)}/chroma_db/{format_name(chatbot_name)}/"
        icon_url = f"{chat_bot_media_url}/default_images/chatbot_image.png"
        chatbot_launcher_icon = f"{chat_bot_media_url}/default_images/avatar-1.png"
        chatbot_background_pattern = f"{chat_bot_media_url}/chatbot_background_patterns/0fac5419_pattern_9.jpg"
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
            icon_url=icon_url,
            chat_bot_media_path =response[1],
            chat_bot_chroma_db_path = response[2],
            user=user,
            chatbot_appearance=chatbot_appearance
        )
        return {"success": "Chatbot added successfully."}   
    
    @staticmethod
    def update_chatbot(user, chatbot_name, chat_id):
        chatbot_data = ChatBotDB.objects.filter(chatbot_id=chat_id).first()
        if not chatbot_data:
            return {"error": "Chatbot not found."}
        if ChatBotDB.objects.filter(user=user, chatbot_name=chatbot_name).exists():
            return {"error": "Chatbot with this name already exists."}
        response = ChatBotService.chat_bot_folder_strucuture(user,chatbot_name)
        """Handles chatbot creation logic."""
        if not  response[0]:
            return {"error": "Something Wrong."}
        try:
            delete_folder(chatbot_data.chat_bot_media_path)
            delete_folder(chatbot_data.chat_bot_chroma_db_path)
        except Exception as e:
            logger.error(f"❌ Error deleting old chatbot directory: {e}")
            return {"error": "Failed to delete old chatbot directory."}
        response = ChatBotService.chat_bot_folder_strucuture(user,chatbot_name)
        if not  response[0]:
            return {"error": "Something Wrong."}
        chat_bot_media_url = f"{format_name(user.username)}/uploads/{format_name(chatbot_name)}/"
        icon_url = f"{chat_bot_media_url}/default_images/chatbot_image.png"
        chatbot_background_pattern = f"{chat_bot_media_url}/chatbot_background_patterns/0fac5419_pattern_9.jpg"
        chatbot_data.chatbot_name = chatbot_name
        chatbot_data.icon_url = icon_url # type: ignore
        chatbot_data.chat_bot_media_path = response[1]
        chatbot_data.chat_bot_chroma_db_path = response[2]
        chatbot_data.save()
        chatbot_appearance = ChatbotAppearance.objects.filter(id=chatbot_data.chatbot_appearance.id).first()
        if chatbot_appearance:
            chatbot_appearance.display_name = chatbot_name
            chatbot_appearance.chatbot_background_pattern = chatbot_background_pattern # type: ignore
            chatbot_appearance.chatbot_image = icon_url # type: ignore
            chatbot_appearance.save()
            return {"success": "Chatbot successfully updated."}
        else:
            return {"error": "Something went wrong with chatbot appearance data."}

    @staticmethod
    def delete_chatbot(chat_id):
        chatbot_data = ChatBotDB.objects.filter(chatbot_id=chat_id).first()
        if not chatbot_data:
            return {"error": "Chatbot not found."}
        try:
            chatbot_data.chatbot_appearance.delete()
            chatbot_data.delete()
            delete_folder(chatbot_data.chat_bot_media_path)
            delete_folder(chatbot_data.chat_bot_chroma_db_path)
        except Exception as e:
            logger.error(f"❌ Error deleting old chatbot directory: {e}")
            return {"error": "Failed to delete old chatbot directory."}
        return {"success": "Chatbot successfully deleted."}
