from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from django.contrib.auth.hashers import make_password
from RAG_CHATBOT_BACKEND_APIS.models import CustomUser
from django.contrib.auth.models import User
import uuid

from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, ChatbotAppearance

fake = Faker()

class Command(BaseCommand):
    help = "Create a user, ChatbotAppearance, and ChatBotDB entry"

    def handle(self, *args, **kwargs):
        chatbot_id = uuid.uuid4()
        openai_key = getattr(settings, "OPENAI_API_KEY", "")  # Use environment variables for security

        # Step 1: Create a single user
        user = CustomUser.objects.create(
            username=fake.user_name(),
            email=fake.email(),
            password=make_password("Password@123")  # Hashing the password
        )

        # Step 2: Print user details
        self.stdout.write(self.style.SUCCESS(
            f"User created: ID = {user}, Username = {user.username}, Email = {user.email}, Password = Password@123"
        ))

        # Step 3: Create ChatbotAppearance entry
        chatbot_appearance = ChatbotAppearance.objects.create(
            chatbot_id=chatbot_id,
            display_name=fake.company()
        )

        self.stdout.write(self.style.SUCCESS(
            f"ChatbotAppearance Created: ID = {chatbot_appearance.chatbot_id}, Display Name = {chatbot_appearance.display_name}"
        ))

        # Step 4: Create ChatBotDB entry
        chatbot_db = ChatBotDB.objects.create(
            chatbot_name="TestBot",
            user=user,  # Assign user instance instead of user.id
            chatbot_appearance=chatbot_appearance,  # Assign instance instead of id
            openai_key=openai_key,
            status=1
        )

        # Step 5: Print chatbot details
        self.stdout.write(self.style.SUCCESS(
            f"ChatBotDB Created: Name = {chatbot_db.chatbot_name}, ID = {chatbot_db.chatbot_id}, Status = {chatbot_db.status}"
        ))
