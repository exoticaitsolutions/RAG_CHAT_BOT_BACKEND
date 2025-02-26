
import logging
import os

from django.db import DatabaseError
from django_filters.exceptions import FieldError

from RAG_Backend import settings
from RAG_CHATBOT_BACKEND_APIS.models import CustomUser
from RAG_CHATBOT_BACKEND_APIS.utils import copy_directory_contents, format_name

logger = logging.getLogger(__name__)
class AuthServices:
    @staticmethod
    def fetch_user_data(key, value):
        try:
            # Validate if 'key' is a valid field in CustomUser
            if not hasattr(CustomUser, key):
                logger.error(f"Invalid field '{key}' for CustomUser model.")
                return None

            user = CustomUser.objects.get(**{key: value})
            return user
        except CustomUser.DoesNotExist:
            logger.warning(f"User with {key}={value} does not exist.")
            return None
        except CustomUser.MultipleObjectsReturned:
            logger.error(f"Multiple users found for {key}={value}. Expected a single record.")
            return None
        except FieldError:
            logger.error(f"Invalid field '{key}' provided. Check your database model.")
            return None
        except DatabaseError as db_err:
            logger.error(f"Database error while fetching user with {key}={value}: {db_err}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching user with {key}={value}: {e}")
            return None


    @staticmethod
    def check_user_existence(key, value):
        try:
            return CustomUser.objects.filter(**{key: value}).exists()
        except FieldError:
            logger.error(f"Invalid field '{key}' provided. Check your database model.")
            return False
        except DatabaseError as db_err:
            logger.error(f"Database error while fetching user with {key}={value}: {db_err}")
            return False
        except Exception as e:
            logger.error(f"Error fetching User with {key}={value}: {e}")
            return False
        
    @staticmethod
    def RegisterUser(username, email, password):
        try:
            user_slug = format_name(username)
            logger.debug(f"user_slug = {user_slug}")

            # Define user-specific directories
            main_user_folder = os.path.join(settings.MEDIA_ROOT, user_slug)
            user_upload_dir = os.path.join(main_user_folder, "uploads")
            user_chroma_db_dir = os.path.join(main_user_folder, "chroma_db")
            user_profile_dir = os.path.join(main_user_folder, "user_profile")
            profile_pic_path = os.path.join(user_profile_dir, "user_profile_pic.jpg")
            # Ensure directories exist
            os.makedirs(user_upload_dir, exist_ok=True)
            os.makedirs(user_chroma_db_dir, exist_ok=True)
            os.makedirs(user_profile_dir, exist_ok=True)
            # User upload URL
            user_upload_url = f"{settings.MEDIA_URL}{user_slug}/uploads/"
            user_chroma_db_url = f"{settings.MEDIA_URL}{user_slug}/uploads/"
            # Copy profile directory (Ensure `settings.COPY_ROOT` exists)
            original_path = os.path.join(settings.COPY_ROOT, "user_profile")
            logger.debug(f"original_path = {original_path}")
            if not copy_directory_contents(original_path, user_profile_dir):
                return False, "Failed to copy user profile directory."
            # Profile image URL
            profile_url = f"{settings.BASE_APP_URL}{settings.MEDIA_URL}{user_slug}/user_profile/user_profile_pic.jpg"
            # Create user
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            # Assign user directories
            user.user_upload_path = user_upload_url
            user.user_chroma_path = user_chroma_db_url
            user.profile_pic = profile_pic_path  # type: ignore # Ensure correct path formatting
            user.profile_url = profile_url
            user.save()
            return True, "User successfully registered."
        
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return False, "Something went wrong"

    @staticmethod
    def UpdateUser_Details(login_user_uuid, user_data,user_profile_data):
        user = AuthServices.fetch_user_data('uuid', login_user_uuid)
        profile_updated = False
        if 'profile_pic' in user_profile_data:
          if user.profile_pic != user_profile_data['profile_pic']:  # type: ignore # Check if the profile pic is different
            user.profile_pic = user_profile_data['profile_pic']  # type: ignore
            user.profile_url = "" # type: ignore
            profile_updated = True  # Mark that profile picture was updated
        for field, value in user_data.items():
            if field == 'profile_pic' and not value:
                continue
            if hasattr(user, field):
              setattr(user, field, value)
              profile_updated = True  # If any other field is updated, mark as updated
        if profile_updated:
            user.save()  # type: ignore
            return True, "User successfully updated."
        return True, "User successfully Updated."
       
        