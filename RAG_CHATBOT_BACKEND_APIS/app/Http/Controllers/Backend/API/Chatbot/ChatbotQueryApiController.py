import logging
from rest_framework.exceptions import JsonResponse
from rest_framework.views import APIView
from RAG_CHATBOT_BACKEND_APIS.app.services.Langchain_Models.LangchainEmbeddingService import LangchainEmbeddingService
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, CustomUser


logger = logging.getLogger(__name__)
class ChatbotQueryApiController(APIView):
    def post(self, request, *args, **kwargs):
        query = request.data.get('query')
        chat_id = request.GET.get("chat_id")
        if not chat_id :
            logger.error("Missing chat_id or user_id")
            return JsonResponse({"status": "failed", "message": "Missing chat_id or user_id"}, status=400)
        if not query:
            return JsonResponse({"error": "Query parameter is missing"}, status=400)
        chatbot = ChatBotDB.objects.filter(chatbot_id=chat_id).first()
        if not chatbot:
            return JsonResponse({"status": "failed", "message": "Invalid chat_id"}, status=404)
        user = CustomUser.objects.get(id=chatbot.user.id)  # type: ignore
        try:
            results = LangchainEmbeddingService.GetResponseFromQuery(chatbot,user,query)
            return JsonResponse({"results": results}, safe=False, status=200)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return JsonResponse({"error": "Internal server error"}, status=500)
       