import logging
import os
import threading
from RAG_CHATBOT_BACKEND_APIS.app.http.Serializers.Modules.Chatbot.ChatbotSerializer import DocumentUploadSerializer
from RAG_CHATBOT_BACKEND_APIS.app.services.Langchain_Models.langchain_llm_models import LangchainEmbeddingService
from RAG_CHATBOT_BACKEND_APIS.models import DocumentNamespaceIds
from RAG_CHATBOT_BACKEND_APIS.utils import create_directories
logger = logging.getLogger(__name__)


class ChatbotContentManagementService:
    @staticmethod
    def upload_and_process_chatbot_documents(login_user_data, chat_bot_details, documents_files):
        uploaded_documents = []  # Add your logic for document upload here
        if len(documents_files) == 0:
            logger.warning("⚠️ No files uploaded!")
            return False, "Please upload at least one file to proceed.", []
        
        for file_key in documents_files.keys():
            uploaded_file = documents_files[file_key]
            file_name = uploaded_file.name
            logger.info(f"📂 Processing file: {file_name}")
            
            smedia_file, media_bot_ = create_directories(str(login_user_data.username), str(chat_bot_details.chatbot_name))
            media_file = os.path.join(smedia_file, 'upload_Documents', file_name)
            # Remove the existing file if it's present
            if os.path.isfile(media_file):
                logger.warning(f"⚠️ Existing file found, removing: {media_file}")
                os.remove(media_file)
            print('media_file', media_file)
            # Check if document already exists in the namespace
            if DocumentNamespaceIds.objects.filter(doc_name=media_file).exists():
                logger.info(f"📜 Document '{file_name}' already exists in the namespace.")
                message = f"Document '{file_name}' already exists!"
                continue  # Skip uploading this document
            # Initialize document_instance to avoid issues if file saving fails
            document_instance = None
            try:
                data = {
                    "user_id": login_user_data.id,
                    "chat_id": chat_bot_details.id,  # type: ignore
                    "filepath": uploaded_file,  # Path to the saved file
                    "name": uploaded_file.name,
                    "size": uploaded_file.size
                }
                
                serializer = DocumentUploadSerializer(data=data)
                if serializer.is_valid():
                    document_instance = serializer.save()
                    uploaded_documents.append(serializer.data)
                    message = f"✅ Document '{file_name}' uploaded successfully!"
                    logger.info(f"✅ Document '{file_name}' uploaded successfully! 🎉")
                    status = True 
                    threading.Thread(target=LangchainEmbeddingService.uploaded_document_and_train_llm, args=(serializer.data, media_file, chat_bot_details, login_user_data,media_bot_)).start()
                    logger.info(f"Started LLM training thread for: {file_name}")
                else:
                    logger.error(f"❌ Document upload failed: {serializer.errors}")
                    message = f"Document upload failed: {serializer.errors}"
                    if document_instance:
                        document_instance.status = "error"
                        document_instance.save()
                    status = False
            except Exception as e:
                logger.error(f"❌ Error saving file {file_name}: {str(e)}")
                message = f"Error saving file {file_name}: {str(e)}"
                if document_instance:
                    document_instance.status = "error"
                    document_instance.save()
                status = False
        
        return status, message, uploaded_documents

    