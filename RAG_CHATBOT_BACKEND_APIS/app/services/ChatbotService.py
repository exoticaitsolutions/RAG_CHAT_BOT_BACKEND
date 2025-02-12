from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB
from django.core.exceptions import ObjectDoesNotExist

def ChatbotDetails(c_id: int, user_id: int):
    """
    Fetches chatbot details based on chatbot ID (c_id) and user ID (user_id).
    Returns a dictionary with chatbot data or None if not found.
    """
    try:
        chatbot_data = ChatBotDB.objects.get(id=c_id, user_id=user_id)
        chatbot_count = ChatBotDB.objects.filter(user_id=user_id).count()
        user_chatbots = list(ChatBotDB.objects.filter(user_id=user_id))  # Convert QuerySet to list for safety
        
        # Constructing the response dictionary
        data = {
            "user_chatbots": user_chatbots,
            "chatbot": chatbot_data,
            "chatbot_count": chatbot_count,
            "chatbot_id": chatbot_data.id, # type: ignore
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
