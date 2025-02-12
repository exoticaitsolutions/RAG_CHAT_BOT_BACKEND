from rest_framework import serializers
from .models import FileUpload,UrlUpload
from RAG_CHATBOT_BACKEND_APIS.models import ChatbotAppearance

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ('id', 'file','uploaded_at', 'created_at', 'updated_at')
        
 
class UrlUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlUpload
        fields = '__all__'
        read_only_fields = ['id', 'embedding_status', 'embedding_error_or_message', 'created_at', 'updated_at']       

class ChatbotAppearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotAppearance
        fields = '__all__'   
