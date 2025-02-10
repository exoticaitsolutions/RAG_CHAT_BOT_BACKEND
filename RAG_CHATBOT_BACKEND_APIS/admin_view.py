from django.shortcuts import render
from django.http import HttpResponse

def admin_login_page(request):
    return render(request, 'admin/auth/login.html')

def admin_register_page(request):
    return render(request, 'admin/auth/register.html')

def admin_dashborad_page(request):
    return render(request, 'admin/page/dashboard.html')



def admin_dashborad_add_assistant_page(request):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/create-chatbot.html')


def admin_dashborad_document_list(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/add-doucument-list.html')

def admin_dashboard_preview_chat_bot(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/preview-chat-page.html')

def admin_dashborad_chatbot_history(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/chat-history.html')


def admin_dashborad_chatbot_setting(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/chat_setting.html')

def admin_dashborad_chatbot_setting_apperence(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/chat_setting_apperence.html')


def admin_dashborad_chatbot_delete(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/chatbot_delete.html')

def admin_dashborad_chatbot_share(request, c_id):  # Add chatbot
    return render(request, 'admin/page/chatbot/pages/share_chat_bot.html')