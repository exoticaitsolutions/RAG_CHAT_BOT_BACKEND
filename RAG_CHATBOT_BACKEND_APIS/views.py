import os
import threading
import logging
import time
import shutil
import hashlib
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ChatbotAppearance

from urllib.parse import urljoin
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
from django.shortcuts import render

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from RAG_CHATBOT_BACKEND_APIS.serializers import FileUploadSerializer, UrlUploadSerializer
from RAG_CHATBOT_BACKEND_APIS.utils import query_chroma, save_pdf_to_chroma,save_url_to_chromadb_threaded 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ChatbotAppearance
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from RAG_CHATBOT_BACKEND_APIS.models import ChatbotAppearance
from RAG_CHATBOT_BACKEND_APIS.serializers import ChatbotAppearanceSerializer

# Logger setup
logger = logging.getLogger(__name__)

# @api_view(['GET', 'PUT'])
# def chatbot_appearance_view(request, chatbot_id):
#     """
#     Get or update chatbot appearance settings.
#     """
#     try:
#         chatbot_appearance = get_object_or_404(ChatbotAppearance, chatbot_id=chatbot_id)

#         if request.method == 'GET':
#             serializer = ChatbotAppearanceSerializer(chatbot_appearance)
#             return Response({
#                 "code": status.HTTP_200_OK,
#                 "message": "Chatbot appearance retrieved successfully.",
#                 "data": serializer.data
#             }, status=status.HTTP_200_OK)

#         elif request.method == 'PUT':
#             serializer = ChatbotAppearanceSerializer(chatbot_appearance, data=request.data, partial=True)

#             if serializer.is_valid():
#                 serializer.save()
#                 logger.info(f"Chatbot appearance updated: {chatbot_id}")
#                 return Response({
#                     "code": status.HTTP_200_OK,
#                     "message": "Chatbot appearance updated successfully.",
#                     "data": serializer.data
#                 }, status=status.HTTP_200_OK)

#             logger.warning(f"Validation failed for chatbot appearance update: {serializer.errors}")
#             return Response({
#                 "code": status.HTTP_400_BAD_REQUEST,
#                 "message": "Invalid data provided.",
#                 "errors": serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e:
#         logger.error(f"Error in chatbot appearance API: {str(e)}")
#         return Response({
#             "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
#             "message": "Internal server error.",
#             "error": str(e)
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Configure logging
# logger = logging.getLogger(__name__)




def save_pdf_to_chroma_threaded(file_upload):
    """
    Saves PDF embeddings to ChromaDB asynchronously.
    """
    try:
        with transaction.atomic():
            file_upload.pdf_embedding_status = "processing"
            file_upload.pdf_embedding_error_or_message = "Processing the PDF embedding"
            file_upload.save()

        pdf_file_path = os.path.join(settings.MEDIA_ROOT, file_upload.file.name)
        logger.info(f'Processing PDF: {pdf_file_path}')
        
        message = save_pdf_to_chroma(pdf_file_path)
        logger.info(f'Embedding Result: {message}')
        
        with transaction.atomic():
            file_upload.pdf_embedding_status = "completed"
            file_upload.pdf_embedding_error_or_message = f"Embeddings stored in ChromaDB for {file_upload.file.name}"
            file_upload.save()

    except Exception as e:
        logger.error(f"Error processing PDF {file_upload.file.name}: {str(e)}")
        with transaction.atomic():
            file_upload.pdf_embedding_status = "failed"
            file_upload.pdf_embedding_error_or_message = str(e)
            file_upload.save()

@swagger_auto_schema(
    methods=['POST'],
    operation_description="Upload a PDF file and store its embeddings in ChromaDB.",
    request_body=FileUploadSerializer,
    responses={
        200: openapi.Response("PDF uploaded successfully", FileUploadSerializer),
        400: openapi.Response("Bad request"),
        500: openapi.Response("Internal server error")
    }
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_pdf_with_loader(request):
    """
    API endpoint to upload a PDF and store embeddings in ChromaDB.
    """
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            file_upload = serializer.save()
            threading.Thread(target=save_pdf_to_chroma_threaded, args=(file_upload,)).start()
            
            response_data = {
                "code": status.HTTP_200_OK,
                "message": "PDF uploaded successfully, and embeddings stored in ChromaDB.",
                "data": {
                    "uploaded_at": file_upload.uploaded_at.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                    "id": str(file_upload.id),
                }
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"error": "Invalid HTTP method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@swagger_auto_schema(
    methods=['POST'],
    operation_description="Query ChromaDB with a natural language search string.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'query': openapi.Schema(type=openapi.TYPE_STRING, description="The search query")
        },
        required=['query']
    ),
    responses={
        200: openapi.Response("Query results"),
        400: openapi.Response("Bad request")
    }
)

@api_view(['POST'])
def upload_url_with_loader(request):
    """
    API endpoint to upload a website URL and store embeddings in ChromaDB.
    """
    if request.method == 'POST':
        url = request.data.get('url')
        if not url:
            return JsonResponse({"error": "No URL provided"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UrlUploadSerializer(data=request.data)
        if serializer.is_valid():
            url_upload = serializer.save()
            threading.Thread(target=save_url_to_chromadb_threaded, args=(url_upload,)).start()

            response_data = {
                "code": status.HTTP_200_OK,
                "message": "URL uploaded successfully, and embeddings are being stored in ChromaDB.",
                "data": {
                    "uploaded_at": url_upload.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                    "id": str(url_upload.id),
                    "url": url_upload.url,
                }
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"error": "Invalid HTTP method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@swagger_auto_schema(
    methods=['POST'],
    operation_description="Query ChromaDB with a natural language search string.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'query': openapi.Schema(type=openapi.TYPE_STRING, description="The search query")
        },
        required=['query']
    ),
    responses={
        200: openapi.Response("Query results"),
        400: openapi.Response("Bad request")
    }
)

@api_view(['POST'])
def ChromaQueryAPIView(request):
    """
    API endpoint to query ChromaDB and return relevant results.
    """
    query = request.data.get('query')

    if not query:
        return JsonResponse({"error": "Query parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        results = query_chroma(query)
        return JsonResponse({"results": results}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def chatbot_view(request):
    return render(request, 'chatbot.html')  



from django.http import JsonResponse
from django.contrib import messages
from .models import ChatbotAppearance
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def chatbot_appearance_form_view(request):
    """
    Handle chatbot appearance settings - Insert or Update without chatbot_id.
    """
    chatbot_appearance, created = ChatbotAppearance.objects.get_or_create(id=1)

    if request.method == "POST":
        chatbot_appearance.display_name = request.POST.get("display-name", chatbot_appearance.display_name)
        chatbot_appearance.footer_name = request.POST.get("footer-name", chatbot_appearance.footer_name)
        chatbot_appearance.initial_message = request.POST.get("initial-message", chatbot_appearance.initial_message)
        chatbot_appearance.chatbot_theme = request.POST.get("chatbot-theme", chatbot_appearance.chatbot_theme)

        # Handle image upload
        if "chatbot_image" in request.FILES:
            chatbot_appearance.chatbot_image = request.FILES["chatbot_image"]

        chatbot_appearance.save()
        
        return JsonResponse({"success": True, "message": "Chatbot appearance updated successfully!"})

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import ChatbotAppearance

# @csrf_exempt  # CSRF token ke bina AJAX request allow karne ke liye
# def chatbot_appearance_form_view(request):
#     """
#     Handle chatbot appearance settings - Insert or Update without chatbot_id.
#     """
#     chatbot_appearance, created = ChatbotAppearance.objects.get_or_create(id=1)

#     if request.method == "POST":
#         chatbot_appearance.display_name = request.POST.get("display-name", chatbot_appearance.display_name)
#         chatbot_appearance.initial_message = request.POST.get("initial-message", chatbot_appearance.initial_message)

#         # Handle image upload
#         if "chatbot_image" in request.FILES:
#             chatbot_appearance.chatbot_image = request.FILES["chatbot_image"]

#         chatbot_appearance.save()
        
#         return JsonResponse({"success": True, "message": "Chatbot appearance updated successfully!"})

#     return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)