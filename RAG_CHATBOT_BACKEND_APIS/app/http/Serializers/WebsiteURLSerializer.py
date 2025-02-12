from rest_framework import serializers

from RAG_CHATBOT_BACKEND_APIS.models import WebsiteDB

class WebsiteURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteDB
        fields = ['user', 'url', 'chatbot', 'no_of_characters', 'no_of_chunks', 'status']
