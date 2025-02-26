import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from functools import wraps
logger = logging.getLogger(__name__)



class AdminDashboardController:
    def admin_dashboard_page(self, request):
        return render(request, "admin/admin_dashboard.html")
