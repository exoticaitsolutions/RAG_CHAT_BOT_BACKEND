from rest_framework import serializers
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, CustomUser, Document


class DocumentUploadSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    chat_id = serializers.IntegerField(write_only=True)
    filepath = serializers.FileField()

    class Meta:
        model = Document
        fields = ['id', 'user_id', 'chat_id', 'filepath', 'name', 'size']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        chat_id = validated_data.pop('chat_id')
        uploaded_file = validated_data.pop('filepath')

        # Extract file name and size
        file_name = uploaded_file.name  # Get file name
        file_size = uploaded_file.size  # Get file size

        # Get user and chatbot
        user = CustomUser.objects.get(id=user_id)
        chatbot = ChatBotDB.objects.get(id=chat_id, user=user)
        # Create and return the document instance
        document = Document.objects.create(
            user=user,
            chatbot=chatbot,
            filepath=uploaded_file,
            name=file_name,  # Save extracted file name
            size=file_size  ,  # Save extracted file size
        )
        return document
