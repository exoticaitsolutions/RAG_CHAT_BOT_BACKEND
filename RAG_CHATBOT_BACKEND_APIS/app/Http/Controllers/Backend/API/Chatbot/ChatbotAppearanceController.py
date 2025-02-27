import logging
from django.http import JsonResponse
from django.views import View
logger = logging.getLogger(__name__)
class ChatbotAppearanceController(View):
    def get(self, request):
        chat_id = request.GET.get("chat_id")
        
        if not chat_id :
            logger.error("Missing chat_id or user_id")
            return JsonResponse({"status": "failed", "message": "Missing chat_id or user_id"}, status=400)
        
        return JsonResponse({"message": "No appearance settings found"}, status=404)

