from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def admin_login_page(request):
    return render(request, 'admin/auth/login.html')

def admin_register_page(request):
    return render(request, 'admin/auth/register.html')

def admin_dashborad_page(request):
    return render(request, 'admin/page/dashboard.html')


@login_required(login_url='/login/')
def admin_dashborad_add_assistant_page(request):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/create-chatbot.html')

@login_required(login_url='/login/')
def admin_dashborad_document_list(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/add-doucument-list.html')

@login_required(login_url='/login/')
def admin_dashboard_preview_chat_bot(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/preview-chat-page.html')

@login_required(login_url='/login/')
def admin_dashborad_chatbot_history(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/chat-history.html')

@login_required(login_url='/login/')
def admin_dashborad_chatbot_setting(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/chat_setting.html')


@login_required(login_url='/login/')
def admin_dashborad_chatbot_setting_apperence(request, c_id):
    # print(f"User authenticated: {request.user.is_authenticated}")  # Debugging
    return render(request, 'admin/page/chatbot/pages/chat_setting_apperence.html')

@login_required(login_url='/login/')
def admin_dashborad_chatbot_delete(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/chatbot_delete.html')

@login_required(login_url='/login/')
def admin_dashborad_chatbot_share(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/share_chat_bot.html')

@login_required(login_url='/login/')
def website_list(request):
    return render(request, 'admin/page/chatbot/pages/add-website-list.html')

# @login_required(login_url='/login/')
def chatbot_view(request):
    return render(request, 'chatbot.html')

  

# http://127.0.0.1:8000/dashboard/services/chatbot/chatbot-appearance/%3Cstr:c_id%3E/