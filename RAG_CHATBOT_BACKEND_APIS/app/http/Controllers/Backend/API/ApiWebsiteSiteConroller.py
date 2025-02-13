import logging
import threading
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from RAG_CHATBOT_BACKEND_APIS.app.http.Serializers.WebsiteURLSerializer import WebsiteURLSerializer
from RAG_CHATBOT_BACKEND_APIS.app.services.training.train_chatbot_urls_service import process_urls_for_training
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, DocumentNamespaceIds, CustomUser

# Configure Logger
logger = logging.getLogger(__name__)

class ApiWebsiteSiteController(APIView):
    @parser_classes([JSONParser])  # Use JSON parser for handling incoming JSON data
    def post(self, request, *args, **kwargs):
        """Handles URL integration with the chatbot"""
        try:
            # Get `chat_id`, `user_id`, and `urls` from the request
            chat_id = request.GET.get("chat_id")
            user_id = request.GET.get("user_id")
            urls = request.data.get("urls", [])

            # Validate input data
            if not chat_id or not user_id or not urls:
                logger.error("Missing chat_id, user_id, or urls")
                return JsonResponse(
                    {"status": "failed", "message": "Missing chat_id, user_id, or urls"},
                    status=400
                )

            # Fetch user object
            user = CustomUser.objects.filter(uuid=user_id).first()
            if not user:
                logger.error(f"User with id {user_id} not found")
                return JsonResponse({"status": "failed", "message": "Invalid user_id"}, status=404)

            # Fetch chatbot object
            chatbot = ChatBotDB.objects.filter(chatbot_id=chat_id, user_id=user.id).first() # type: ignore
            if not chatbot:
                logger.error(f"Chatbot with id {chat_id} not found for user {user_id}")
                return JsonResponse({"status": "failed", "message": "Invalid chat_id"}, status=404)

            # Initialize variables
            no_of_characters = 0
            no_of_chunks = 0
            uploaded_documents = []

            # Process each URL
            for urllist in urls:
                data = {
                    "user": user.id,  # Pass the user ID instead of an object # type: ignore
                    "url": urllist,
                    "chatbot": chatbot.id,  # Pass the chatbot ID instead of an object # type: ignore
                    "no_of_characters": no_of_characters,
                    "no_of_chunks": no_of_chunks,
                    "status": "pending"
                }
                serializer = WebsiteURLSerializer(data=data)
                if serializer.is_valid():
                    document_instance = serializer.save()
                    uploaded_documents.append(serializer.data)
                    logger.info("Website URL inserted successfully")
                    try:
                        threading.Thread(target=process_urls_for_training, args=(urllist,chatbot, user,document_instance.id,)).start()
                        logger.info(f"Started LLM training thread for: {urllist}")
                    except Exception as e:
                        logger.error(f"Failed to start thread for document {urllist}: {str(e)}")
                        document_instance.status = "error"
                        document_instance.save()
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
