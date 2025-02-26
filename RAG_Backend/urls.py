"""
URL configuration for RAG_Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Uncomment the line below if you want to redirect the root URL to '/login/'
    # path('', RedirectView.as_view(url='/login/', permanent=False)),
    # Main application URLs
    path("", include("RAG_CHATBOT_BACKEND_APIS.urls")),
    path("api/v2/", include("RAG_CHATBOT_BACKEND_APIS.api_routes")),
]
