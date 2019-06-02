from django.shortcuts import render, redirect
from .models import *


# Create your views here.

def message(request, uid):
    if request.session.get('is_login'):
        from_user = sf_models.User.objects.get(id=request.session.get('uid'))
        try:
            to_user = sf_models.User.objects.get(id=uid)
        except:
            return render(request, 'confirm.html', {'title': "错误", "message": "该用户不存在"})
            
        if from_user == to_user:
            return render(request, 'confirm.html', {'title': "错误", "message": "不允许自己与自己聊天"})
        RecentContacts.objects.update_or_create(user1=from_user, user2=to_user)
        return render(request, 'message.html',
                      {'recent': from_user.my_recent_contacts.all().order_by('-last_view_time'),
                       'current_contact': to_user})
    else:
        return render(request, 'confirm.html', {'title': "错误", "message": "请登录"})
