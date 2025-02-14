import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB

logger = logging.getLogger(__name__)

class AdminDashboardController:
    @method_decorator(login_required(login_url='/login/'))
    def admin_dashboard_page(self, request):
        user_id = request.user.id
        logger.info(f"📩 Received request user_id: {user_id}")

        chatbots = ChatBotDB.objects.filter(user=user_id)
        context = {"chatbot": chatbots, "data": {"user_chatbots": chatbots}}
        return render(request, "admin/admin_dashboard.html", context)
