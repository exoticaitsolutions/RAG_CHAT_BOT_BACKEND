import logging
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from RAG_CHATBOT_BACKEND_APIS.app.http.Serializers.WebsiteURLSerializer import WebsiteURLSerializer
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, DocumentNamespaceIds
# Configure Logger
logger = logging.getLogger(__name__)

class ApiWebsiteSiteConroller(APIView):
    @parser_classes([JSONParser])  # Use JSON parser for handling incoming JSON data
    def post(self, request, *args, **kwargs):
        """Handles URL integration with the chatbot"""
        try:
            # Get `chat_id` and `user_id` from the request
            chat_id = request.GET.get("chat_id")
            user_id = request.GET.get("user_id")
            urls = request.data.get('urls', [])
            if not chat_id or not user_id  or not urls :
                logger.error("Missing chat_id or user_id and urls")
                return JsonResponse({"status": "failed", "message": "Missing chat_id or user_id"}, status=400)
            try:
                chat_id = int(chat_id)
                user_id = int(user_id)
            except ValueError:
                logger.error("Invalid format for chat_id or user_id")
                return JsonResponse({"status": "failed", "message": "Invalid chat_id or user_id format"}, status=400)
            # Get the list of URLs from the request data
            logger.info(f"Received URLs: {urls}")
            print(f"Received URLs: {urls}")
            chatbot = ChatBotDB.objects.filter(id=chat_id, user_id=user_id).first()
            if not chatbot:
                logger.error(f"Chatbot with id {chat_id} not found for user {user_id}")
                return JsonResponse({"status": "failed", "message": "Invalid chat_id"}, status=404)
            # Validate user existence
            user = User.objects.filter(id=user_id).first()
            if not user:
                logger.error(f"User with id {user_id} not found")
                return JsonResponse({"status": "failed", "message": "Invalid user_id"}, status=404)
            no_of_characters = 0
            no_of_chunks = 0
            uploaded_documents = []
            for  urllist in urls:
                data = {
                    "user": user_id,
                    "url": urllist,
                    "chatbot": chat_id,
                    "no_of_characters": no_of_characters,
                    "no_of_chunks": no_of_chunks,
                    "status":"pending"
                }
                print(f'data is {data}')
                serializer = WebsiteURLSerializer(data=data)
                if serializer.is_valid():
                    document_instance = serializer.save()
                    uploaded_documents.append(serializer.data)
                    logger.info(f"Website url  inserted successfully")
                else:
                    logger.error(f"Document upload failed: {serializer.errors}")
                    return JsonResponse({"status": "failed", "errors": serializer.errors}, status=400)
                
            # Return success response
            return JsonResponse({
                "status": "success",
                "message": "Documents uploaded and saved successfully",
                "uploaded_files": uploaded_documents
            }, status=201)
        except Exception as e:
            # Log the exception
            logger.error(f"Error in URL integration: {str(e)}")

            return JsonResponse(
                {"status": "failed", "message": "An unexpected error occurred."},
                status=500
            )
