import logging
from django.shortcuts import render
from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger(__name__)
class DocumentController:
    def show_upload_form(self, request, c_id):
        """ Renders the document upload form """
        return render(request, 'admin/page/chatbot/pages/add-doucument-list.html')
    # Configure Logger


    def upload_and_train(self, request, c_id):
        chat_id = c_id
        user_id = request.user.id
        url = f"http://127.0.0.1:8000/api/v1/upload/pdf/?chat_id={chat_id}&user_id={user_id}"
        payload = {}

        # Check if request method is POST and there are files
        if request.method == 'POST' and len(request.FILES) != 0:
            files = []
            # Iterate over all uploaded files
            for file_key in request.FILES:
                uploaded_file = request.FILES[file_key]
                file_path = f'/tmp/{uploaded_file.name}'
                try:
                    with open(file_path, 'wb') as f:
                        for chunk in uploaded_file.chunks():
                            f.write(chunk)
                    # Add the file to the files list
                    files.append(('file', (uploaded_file.name, open(file_path, 'rb'), uploaded_file.content_type)))
                    logger.info(f"File {uploaded_file.name} saved to {file_path}")
                except Exception as e:
                    logger.error(f"Error saving file {uploaded_file.name}: {str(e)}")
                    return JsonResponse({"status": "failed", "message": "Error saving file"}, status=500)

            logger.info(f"Files to be trained on: {files}")
            headers = {}
            try:
                # Make the POST request to the upload endpoint
                response = requests.post(url, headers=headers, data=payload, files=files)
                # Parse JSON response if it's in JSON format
                try:
                    response_json = response.json()
                except ValueError:
                    logger.error(f"Invalid JSON response: {response.text}")
                    response_json = None

                # Check the response status and log accordingly
                if response.status_code == 200:
                    logger.info(f"Successfully uploaded and trained documents. Response: {response_json}")
                    return JsonResponse({
                        "status": "success",
                        "message": "Files uploaded and training started successfully",
                        "response": response_json
                    }, status=200)
                elif response.status_code == 400:
                    logger.error(f"Bad request: {response_json}")
                    return JsonResponse({
                        "status": "failed",
                        "message": "Bad request, check the uploaded files or parameters",
                        "response": response_json
                    }, status=400)
                elif response.status_code == 500:
                    logger.error(f"Server error: {response_json}")
                    return JsonResponse({
                        "status": "failed",
                        "message": "Server error occurred during document processing",
                        "response": response_json
                    }, status=500)
                else:
                    logger.warning(f"Unexpected response status: {response.status_code}. Response: {response_json}")
                    return JsonResponse({
                        "status": "failed",
                        "message": f"Unexpected error occurred. Status code: {response.status_code}",
                        "response": response_json
                    }, status=response.status_code)

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {str(e)}")
                return JsonResponse({
                    "status": "failed",
                    "message": "Error making the request to upload and train documents",
                    "error_details": str(e)
                }, status=500)

        # If no files are uploaded
        return JsonResponse({
            "status": "failed",
            "message": "No files uploaded"
        }, status=400)


    