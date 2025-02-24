import logging
import os
from concurrent.futures import ThreadPoolExecutor
from RAG_CHATBOT_BACKEND_APIS.app.Http.Serializers.Modules.Chatbot.document_website_serializers import DocumentUploadSerializer, WebsiteURLSerializer
from RAG_CHATBOT_BACKEND_APIS.app.services.Langchain_Models.LangchainEmbeddingService import LangchainEmbeddingService
from RAG_CHATBOT_BACKEND_APIS.utils import create_directories

logger = logging.getLogger(__name__)

# Define a ThreadPoolExecutor with a limited number of worker threads
executor = ThreadPoolExecutor(max_workers=5)

class ChatbotContentManagementService:
    @staticmethod
    def upload_and_process_chatbot_website_urls(user, chatbot, urls):
        """
        Uploads website URLs for chatbot training and starts processing.
        """
        logger.info(f"📥 Uploading website URLs for chatbot: {chatbot.chatbot_name}")
        
        # Prepare data for serialization
        data = {"user": user.id, "url": urls, "chatbot": chatbot.id, "no_of_characters": 0, "no_of_chunks": 0, "status": "pending"}
        serializer = WebsiteURLSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            website_instance = serializer.save()
            logger.info("✅ Website URL inserted successfully")
            
            # Create necessary directories for media storage
            media_path, bot_path = create_directories(user.username, chatbot.chatbot_name)
            
            # Submit task to ThreadPoolExecutor
            executor.submit(LangchainEmbeddingService.process_urls_for_training, website_instance.id, chatbot, user, bot_path)
            logger.info("🚀 Started LLM training thread for website URLs")
            
            return True, "Website URL inserted successfully", serializer.data
        
        logger.error(f"❌ Website URL upload failed: {serializer.errors}")
        return False, f"Website URL upload failed: {serializer.errors}", []

    @staticmethod
    def upload_and_process_chatbot_documents(user, chatbot, files):
        """
        Uploads and processes chatbot documents for training.
        """
        if not files:
            logger.warning("⚠️ No files uploaded!")
            return False, "No files uploaded.", []
        
        uploaded_docs = []
        
        # Create directories for storing uploaded documents
        media_path, bot_path = create_directories(user.username, chatbot.chatbot_name)
        
        for file in files.values():
            file_path = os.path.join(media_path, 'upload_Documents', file.name)
            logger.info(f"📂 Processing file: {file.name}")
        
            try:
                # Prepare data for serialization
                serializer = DocumentUploadSerializer(data={"user_id": user.id, "chat_id": chatbot.id, "filepath": file, "name": file.name, "size": file.size})
                
                if serializer.is_valid():
                    serializer.save()
                    uploaded_docs.append(serializer.data)
                    logger.info(f"✅ Document '{file.name}' uploaded successfully!")
                    
                    # Submit task to ThreadPoolExecutor
                    executor.submit(
                        LangchainEmbeddingService.uploaded_document_and_train_llm,
                        serializer.data, file_path, chatbot, user, bot_path
                    )
                    logger.info(f"🚀 Started LLM training thread for: {file.name}")
            except Exception as e:
                logger.error(f"❌ Error saving file {file.name}: {str(e)}")
        
        return bool(uploaded_docs), "Upload completed.", uploaded_docs
