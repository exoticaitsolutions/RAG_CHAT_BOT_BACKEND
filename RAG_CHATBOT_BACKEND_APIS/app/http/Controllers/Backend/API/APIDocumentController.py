import logging
import os
import socket
import threading
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes

from RAG_CHATBOT_BACKEND_APIS.app.http.Serializers.DocumentUpload import DocumentUploadSerializer
from RAG_CHATBOT_BACKEND_APIS.app.services.training.train_document import uploaded_document_and_train_llm
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, DocumentNamespaceIds

# Configure Logger
logger = logging.getLogger(__name__)

class APIDocumentController(APIView):
    @parser_classes([MultiPartParser, FormParser])
    def post(self, request, *args, **kwargs):
        """Handles PDF document uploads and triggers LLM training."""
        logger.info("Received document upload request")

        # Get `chat_id` and `user_id` from the request
        chat_id = request.GET.get("chat_id")
        user_id = request.GET.get("user_id")

        if not chat_id or not user_id:
            logger.error("Missing chat_id or user_id")
            return JsonResponse({"status": "failed", "message": "Missing chat_id or user_id"}, status=400)

        try:
            chat_id = int(chat_id)
            user_id = int(user_id)
        except ValueError:
            logger.error("Invalid format for chat_id or user_id")
            return JsonResponse({"status": "failed", "message": "Invalid chat_id or user_id format"}, status=400)

        # Validate chatbot existence
        chatbot = ChatBotDB.objects.filter(id=chat_id, user_id=user_id).first()
        if not chatbot:
            logger.error(f"Chatbot with id {chat_id} not found for user {user_id}")
            return JsonResponse({"status": "failed", "message": "Invalid chat_id"}, status=404)

        # Validate user existence
        user = User.objects.filter(id=user_id).first()
        if not user:
            logger.error(f"User with id {user_id} not found")
            return JsonResponse({"status": "failed", "message": "Invalid user_id"}, status=404)

        # Check if files were uploaded
        if len(request.FILES) == 0:
            logger.error("No files uploaded")
            return JsonResponse({"status": "failed", "message": "No files uploaded"}, status=400)

        uploaded_documents = []

        try:
            for inc_var, file_key in enumerate(request.FILES.keys()):
                uploaded_file = request.FILES[file_key]  # Get the file object
                file_name = uploaded_file.name  # Get file name
                
                logger.info(f"Processing file: {file_name}")

                # Construct file path
                media_file = os.path.join(settings.MEDIA_ROOT, 'uploads', str(user.username), str(chatbot.chatbot_name), file_name)
                logger.debug(f"Constructed media file path: {media_file}")

                # Remove existing file
                if os.path.isfile(media_file):
                    logger.warning(f"Existing file found, removing: {media_file}")
                    os.remove(media_file)

                # Check if document already exists
                if DocumentNamespaceIds.objects.filter(doc_name=media_file).exists():
                    logger.info(f"Document {file_name} already exists in namespace")
                
                # Prepare serializer data
                data = {
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "filepath": uploaded_file,
                    "name": uploaded_file.name,
                    "size": uploaded_file.size
                }

                serializer = DocumentUploadSerializer(data=data)
                if serializer.is_valid():
                    document_instance = serializer.save()
                    uploaded_documents.append(serializer.data)
                    logger.info(f"Document {file_name} uploaded successfully")
                    
                    # Start document processing in a separate thread
                    try:
                        threading.Thread(target=uploaded_document_and_train_llm, args=(serializer.data, media_file, chatbot, user)).start()
                        logger.info(f"Started LLM training thread for: {file_name}")
                    except Exception as e:
                        logger.error(f"Failed to start thread for document {file_name}: {str(e)}")
                        document_instance.status = "error"
                        document_instance.save()

                else:
                    logger.error(f"Document upload failed: {serializer.errors}")
                    return JsonResponse({"status": "failed", "errors": serializer.errors}, status=400)

            return JsonResponse({
                "status": "success",
                "message": "Documents uploaded and saved successfully",
                "uploaded_files": uploaded_documents
            }, status=201)

        except socket.error as e:
            logger.error(f"Socket error encountered: {str(e)}")
            return JsonResponse({"status": "failed", "message": "Network error occurred"}, status=500)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"status": "failed", "message": "An unexpected error occurred"}, status=500)
