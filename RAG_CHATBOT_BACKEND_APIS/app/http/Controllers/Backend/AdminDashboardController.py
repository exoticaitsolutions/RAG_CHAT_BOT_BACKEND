import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render

logger = logging.getLogger(__name__)

class AdminDashboardController:
    @method_decorator(login_required(login_url='/login/'))
    def admin_dashboard_page(self, request):
        return render(request, "admin/admin_dashboard.html")
