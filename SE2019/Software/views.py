import datetime
import hashlib
import os

from django.conf import settings
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from django.db.models import Q
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from captcha.models import CaptchaStore
from django.http import HttpResponse

from .forms import *
from .models import *


# Create your views here.
def index(request):
#    print(get_host_ip())
    return render(request, 'index.html')


def space(request, uid):
    #try:
        user = User.objects.get(id=uid)
        current_user = None
#        dynamics = []
        count_of_new_dynamic = 0
        if request.session.get('is_login'):
            current_user = User.objects.get(id=request.session.get('uid'))
            '''dynamics = [x for x in DynamicRecord.objects.filter(Q(project__in=current_user.favorite_projects.all()) | Q(project__creator__in=current_user.follower.all())) if
                        ((
                                 x.project in current_user.favorite_projects.all() and x.time_of_dynamic > ProjectAttention.objects.get(
                             project=x.project, follower=current_user).time) or
                         (
                                 x.project.creator in current_user.follower.all() and x.time_of_dynamic > UserAttention.objects.get
                         (user=x.project.creator,
                          follower=current_user).time and x.typ == 1)) and x.time_of_dynamic > current_user.last_view_dynamic]'''
            cursor = connection.cursor()
            cursor.execute(
                "select count(*) from DB4Django.Software_dynamicrecord "
                "where ((time_of_dynamic>("
                "select DB4Django.Software_userattention.time "
                "from DB4Django.Software_userattention join DB4Django.Software_project "
                "on (DB4Django.Software_userattention.follower_id = %s and DB4Django.Software_userattention.user_id = DB4Django.Software_project.creator_id) "
                "where DB4Django.Software_project.pid=DB4Django.Software_dynamicrecord.project_id) and typ=1) "
                "or time_of_dynamic>("
                "select time from DB4Django.Software_projectattention "
                "where DB4Django.Software_dynamicrecord.project_id = project_id and follower_id = %s)) "
                "and time_of_dynamic>%s",[current_user.id,current_user.id,current_user.last_view_dynamic])
            count_of_new_dynamic = cursor.fetchone()[0]
        if request.method == 'POST':
            if not request.session.get('is_login'):
                return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
            if request.POST.get('feature') == '关注':
                UserAttention.objects.get_or_create(follower=current_user, user=user)
            elif request.POST.get('feature') == '取消关注':
                UserAttention.objects.filter(follower=current_user, user=user).delete()
        judge = False  # 判断是否已经关注
        if current_user in user.follower_of_user.all():
            judge = True

        return render(request, 'space.html',
                      {'user': user, 'judge': judge, 'count_of_new_dynamic': count_of_new_dynamic})
    #except:
    #    return render(request, 'confirm.html', {'title': '错误', 'message': '用户不存在'})


def fans(request, uid):
    try:
        user = User.objects.get(id=uid)
        current_user = None
        count_of_new_dynamic = 0
        if request.session.get('is_login'):
            current_user = User.objects.get(id=request.session.get('uid'))
        if request.session.get('uid')==uid:
            cursor = connection.cursor()
            cursor.execute(
                "select count(*) from DB4Django.Software_dynamicrecord "
                "where ((time_of_dynamic>("
                "select DB4Django.Software_userattention.time "
                "from DB4Django.Software_userattention join DB4Django.Software_project "
                "on (DB4Django.Software_userattention.follower_id = %s and DB4Django.Software_userattention.user_id = DB4Django.Software_project.creator_id) "
                "where DB4Django.Software_project.pid=DB4Django.Software_dynamicrecord.project_id) and typ=1) "
                "or time_of_dynamic>("
                "select time from DB4Django.Software_projectattention "
                "where DB4Django.Software_dynamicrecord.project_id = project_id and follower_id = %s)) "
                "and time_of_dynamic>%s",[current_user.id,current_user.id,current_user.last_view_dynamic])
            count_of_new_dynamic = cursor.fetchone()[0]
        if request.method == 'POST':
            if not request.session.get('is_login'):
                return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
            if request.POST.get('feature') == '关注':
                UserAttention.objects.get_or_create(follower=current_user,
                                                    user=User.objects.get(id=request.POST.get('uid')))
            elif request.POST.get('feature') == '取消关注':
                UserAttention.objects.filter(follower=current_user,
                                             user=User.objects.get(id=request.POST.get('uid'))).delete()
        return render(request, 'fans.html', {'user': user, 'current_user': current_user,'count_of_new_dynamic':count_of_new_dynamic})
    except:
        return render(request, 'confirm.html', {'title': '错误', 'message': '用户不存在'})


def follow(request, uid):
    try:
        user = User.objects.get(id=uid)
        current_user = None
        count_of_new_dynamic = 0
        if request.session.get('is_login'):
            current_user = User.objects.get(id=request.session.get('uid'))
        if request.session.get('uid')==uid:
            cursor = connection.cursor()
            cursor.execute(
                "select count(*) from DB4Django.Software_dynamicrecord "
                "where ((time_of_dynamic>("
                "select DB4Django.Software_userattention.time "
                "from DB4Django.Software_userattention join DB4Django.Software_project "
                "on (DB4Django.Software_userattention.follower_id = %s and DB4Django.Software_userattention.user_id = DB4Django.Software_project.creator_id) "
                "where DB4Django.Software_project.pid=DB4Django.Software_dynamicrecord.project_id) and typ=1) "
                "or time_of_dynamic>("
                "select time from DB4Django.Software_projectattention "
                "where DB4Django.Software_dynamicrecord.project_id = project_id and follower_id = %s)) "
                "and time_of_dynamic>%s",[current_user.id,current_user.id,current_user.last_view_dynamic])
            count_of_new_dynamic = cursor.fetchone()[0]
        if request.method == 'POST':
            if not request.session.get('is_login'):
                return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
            if request.POST.get('feature') == '关注':
                UserAttention.objects.get_or_create(follower=current_user,
                                                    user=User.objects.get(id=request.POST.get('uid')))
            elif request.POST.get('feature') == '取消关注':
                UserAttention.objects.filter(follower=current_user,
                                             user=User.objects.get(id=request.POST.get('uid'))).delete()
        return render(request, 'follow.html', {'user': user, 'current_user': current_user,'count_of_new_dynamic':count_of_new_dynamic})
    except:
        return render(request, 'confirm.html', {'title': '错误', 'message': '用户不存在'})


def dynamic(request):
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    current_user = User.objects.get(id=request.session.get('uid'))
    '''dynamics = [x for x in DynamicRecord.objects.filter(Q(project__in=current_user.favorite_projects.all()) | Q(project__creator__in=current_user.follower.all())) if
                (x.project in current_user.favorite_projects.all() and x.time_of_dynamic > ProjectAttention.objects.get(
                    project=x.project, follower=current_user).time) or
                (x.project.creator in current_user.follower.all() and x.time_of_dynamic > UserAttention.objects.get
                (user=x.project.creator, follower=current_user).time and x.typ == 1)]'''
    dynamics = DynamicRecord.objects.raw(
        "select * from DB4Django.Software_dynamicrecord "
        "where (time_of_dynamic>("
        "select DB4Django.Software_userattention.time "
        "from DB4Django.Software_userattention join DB4Django.Software_project "
        "on (DB4Django.Software_userattention.follower_id = %s and DB4Django.Software_userattention.user_id = DB4Django.Software_project.creator_id) "
        "where DB4Django.Software_project.pid=DB4Django.Software_dynamicrecord.project_id) and typ=1) "
        "or time_of_dynamic>("
        "select time from DB4Django.Software_projectattention "
        "where DB4Django.Software_dynamicrecord.project_id = project_id and follower_id = %s) ORDER BY time_of_dynamic DESC"
        , [current_user.id, current_user.id])
    current_user.last_view_dynamic = timezone.now()
    current_user.save()
    return render(request, 'dynamic.html', {'dynamics': dynamics,
                                            'user': current_user})


HISTORY_NUM = 25
def history(request):
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    user = User.objects.get(id=request.session.get('uid'))
    if request.method == 'POST':
        if request.POST.get('feature') == '清空历史':
            user.myhistory.all().delete()
        elif request.POST.get('feature') == '删除历史':
            user.myhistory.filter(project_id=request.POST.get('pid')).delete()
    history_list = user.myhistory.all().order_by('-time')
    paginator = Paginator(history_list, HISTORY_NUM)
    page = request.GET.get('page')
    try:
        projs = paginator.page(page)
        page_num = page
    except PageNotAnInteger:
        projs = paginator.page(1)
        page_num = 1
    except EmptyPage:
        projs = paginator.page(paginator.num_pages)
        page_num = paginator.num_pages
    return render(request, 'history.html',{'paginator': paginator, 'page':paginator.page(page_num), 'user':user})


def history_origin(request):
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    user = User.objects.get(id=request.session.get('uid'))
    if request.method == 'POST':
        if request.POST.get('feature') == '清空历史':
            user.myhistory.all().delete()
        elif request.POST.get('feature') == '删除历史':
            user.myhistory.filter(project_id=request.POST.get('pid')).delete()
    return render(request, 'history.html', {'user': user})


def release_project(request):
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    elif User.objects.get(id=request.session.get('uid')).identity:
        return render(request, 'confirm.html', {'title': '错误', 'message': '投资人无法创建项目'})
    current_user = User.objects.get(id=request.session.get('uid'))
    cursor = connection.cursor()
    cursor.execute(
                "select count(*) from DB4Django.Software_dynamicrecord "
                "where ((time_of_dynamic>("
                "select DB4Django.Software_userattention.time "
                "from DB4Django.Software_userattention join DB4Django.Software_project "
                "on (DB4Django.Software_userattention.follower_id = %s and DB4Django.Software_userattention.user_id = DB4Django.Software_project.creator_id) "
                "where DB4Django.Software_project.pid=DB4Django.Software_dynamicrecord.project_id) and typ=1) "
                "or time_of_dynamic>("
                "select time from DB4Django.Software_projectattention "
                "where DB4Django.Software_dynamicrecord.project_id = project_id and follower_id = %s)) "
                "and time_of_dynamic>%s",[current_user.id,current_user.id,current_user.last_view_dynamic])
    count_of_new_dynamic = cursor.fetchone()[0]
    form = Form4ProjectRelease()
    if request.method == 'POST':
        form = Form4ProjectRelease(request.POST, request.FILES)
        area = ','.join(form.__getitem__('area').data)
        if form.is_valid():
            project = Project()
            info = form.cleaned_data
            project.name = info['name']
            project.company_name = info['company']
            project.area = ",".join(info['area'])
            project.introduction = info['introduction']
            project.detailed_introduction = info['detailed_introduction']
            project.location = info['location']
            project.proposal = info['proposal']
            if project.proposal:
                if project.proposal.size>10485760:
                    message = "文件过大，需小于10MB"
                    return render(request, 'release_project.html', {'Form4ProjectRelease': form,'user':current_user,'count_of_new_dynamic':count_of_new_dynamic,'message':message,'area':area})
            project.creator = User.objects.get(id=request.session.get('uid'))
            # project.creator = User.objects.get(id=1)  # for test
            project.recruit = info['recruit']
            project.security_level = info['security_level']
            project.status = info['status']
            project.save()
            DynamicRecord.objects.create(project=project, typ=1)
            return render(request, 'confirm.html', {'title': '成功', 'message': '创建项目成功，即将跳转至主页'})
        else:
            return render(request, 'release_project.html', {'Form4ProjectRelease': form,'user':current_user,'count_of_new_dynamic':count_of_new_dynamic,'area':area})
            
    return render(request, 'release_project.html', {'Form4ProjectRelease': form,'user':current_user,'count_of_new_dynamic':count_of_new_dynamic})


def modify_project(request, pid):
    try:
        if not request.session.get('is_login'):
            return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
        elif Project.objects.get(pid=pid).creator_id != request.session.get('uid'):
            return render(request, 'confirm.html', {'title': '错误', 'message': '该项目不是由您发起的，无法修改'})
    except:
        return render(request, 'confirm.html', {'title': '错误', 'message': '项目不存在'})
    project = Project.objects.get(pid=pid)
    if request.method == 'POST':
        form_info = Form4ProjectModify(request.POST, request.FILES)

        #area = ','.join(form_info.__getitem__('area').data)
        if form_info.is_valid():
            info = form_info.cleaned_data
            project.company_name = info['company']
            project.area = ",".join(info['area'])
            project.introduction = info['introduction']
            project.detailed_introduction = info['detailed_introduction']
            project.location = info['location']
            if info['proposal'] is not None:
                if info['proposal'].size>10485760:
                    message = "文件过大，需小于10MB"
                    return render(request, 'modify_project.html', {'Form4Project': form_info,'message':message,'Project':project})
                if project.proposal:
                    os.remove(project.proposal.path)
                project.proposal = info['proposal']
            project.recruit = info['recruit']
            project.security_level = info['security_level']
            project.status = info['status']
            project.save()
            DynamicRecord.objects.create(project=project, typ=0)
            return render(request, 'confirm.html', {'title': '成功', 'message': '修改项目信息成功，即将跳转至主页'})
        return render(request, 'modify_project.html', {'Form4Project': form_info,'Project':project,})
    else:
        form = Form4ProjectModify(initial={'company': project.company_name,
                                           'area':
                                               [int(i) for i in
                                                project.area.split(',')],
                                           'introduction': project.introduction,
                                           'detailed_introduction': project.detailed_introduction,
                                           'status': project.status, 'recruit': project.recruit,
                                           'security_level': project.security_level, 'location': project.location})
        return render(request, 'modify_project.html', {'Form4Project': form, 'Project': project})


PROJ_NUM_IN_ONE_PAGE = 6
def project_list(request):
    level = 0
    if request.session.get('is_login'):
        level = User.objects.get(id = request.session.get('uid')).level
        proj_list = Project.objects.filter(Q(security_level__lte=level)|Q(creator_id=request.session.get('uid'))).order_by('-time')
    else:
        proj_list = Project.objects.filter(security_level__lte=level).order_by('-time')
    paginator = Paginator(proj_list, PROJ_NUM_IN_ONE_PAGE)
    page = request.GET.get('page')
    try:
        projs = paginator.page(page)
        page_num = page
    except PageNotAnInteger:
        projs = paginator.page(1)
        page_num = 1
    except EmptyPage:
        projs = paginator.page(paginator.num_pages)
        page_num = paginator.num_pages
    return render(request, 'project_list.html', {'paginator': paginator, 'page':paginator.page(page_num)})


def project_list_origin(request):
    return render(request, 'project_list.html', {'ProjectsList': Project.objects.all()})


'''MY_PROJ_NUM = 60
def my_projects(request, uid):
    try:
        user = User.objects.get(id=uid)
        if user.identity:
            return render(request, 'confirm.html', {'title': '错误', 'message': '投资人无项目'})
        proj_list = Project.objects.filter(creator_id=uid)
        paginator = Paginator(proj_list, MY_PROJ_NUM)
        page = request.GET.get('page')
        try:
            projs = paginator.page(page)
            page_num = page
        except PageNotAnInteger:
            projs = paginator.page(1)
            page_num = 1
        except EmptyPage:
            projs = paginator.page(paginator.num_pages)
            page_num = paginator.num_pages
        return render(request, 'my_projects.html',
                      {'paginator': paginator, 'page':paginator.page(page_num), 'user': user
                       })
    except:
        return render(request, 'confirm.html', {'title': '错误', 'message': '用户不存在'})'''


def my_projects(request, uid):
    #try:
        user = User.objects.get(id=uid)
        count_of_new_dynamic = 0
        if user.identity:
            return render(request, 'confirm.html', {'title': '错误', 'message': '投资人无项目'})
        if request.session.get('is_login'):
            current_user = User.objects.get(id=request.session.get('uid'))
            cursor = connection.cursor()
            cursor.execute(
                "select count(*) from DB4Django.Software_dynamicrecord "
                "where ((time_of_dynamic>("
                "select DB4Django.Software_userattention.time "
                "from DB4Django.Software_userattention join DB4Django.Software_project "
                "on (DB4Django.Software_userattention.follower_id = %s and DB4Django.Software_userattention.user_id = DB4Django.Software_project.creator_id) "
                "where DB4Django.Software_project.pid=DB4Django.Software_dynamicrecord.project_id) and typ=1) "
                "or time_of_dynamic>("
                "select time from DB4Django.Software_projectattention "
                "where DB4Django.Software_dynamicrecord.project_id = project_id and follower_id = %s)) "
                "and time_of_dynamic>%s",[current_user.id,current_user.id,current_user.last_view_dynamic])
            count_of_new_dynamic = cursor.fetchone()[0]
        return render(request, 'my_projects.html',
                      {'count_of_new_dynamic': count_of_new_dynamic, 'user': user
                       })
    #except:
    #    return render(request, 'confirm.html', {'title': '错误', 'message': '用户不存在'})



def project_info(request, pid):
    try:
        project = Project.objects.get(pid=pid)
    except:
        return render(request, 'confirm.html', {'title': '错误', 'message': '项目不存在'})
    user = None
    level = 0
    if request.session.get('is_login'):
        user = User.objects.get(id=request.session.get('uid'))
        if project.creator==user:
            level = 3
        else:
            level = user.level
        if project.security_level<=level:
            History.objects.update_or_create(user=user, project=project)
    if project.security_level>level:
        return render(request, 'confirm.html', {'title': '抱歉', 'message': '您的权限不足'})
    if request.method == "POST":
        if not request.session.get('is_login'):
            return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
        if request.POST.get('feature') == '收藏':
            ProjectAttention.objects.get_or_create(follower=user, project=project)
            return JsonResponse(data={'msg': 'collect'})
        elif request.POST.get('feature') == '取消收藏':
            ProjectAttention.objects.filter(follower=user, project=project).delete()
            return JsonResponse(data={'msg': 'de-collect'})
    collected = False  # 判断是否已经收藏该项目
    if user in project.favorite_projects.all():
        collected = True
    area_of_project = [AREA_CHOICES[int(i)][1] for i in
                       project.area.split(',')]

    ######## 推荐系统
    recommend_proj = []
    if request.session.get('is_login'):
        # 登录的用户才给推荐
        from .recommend import recommend
        h = History.objects.filter(user_id=user.id).values_list('project__area','time')
        recommend_proj = recommend(user.area, h, Project.objects.all())
        # print()
    ######## 推荐系统
    return render(request, "project_info.html",
                  {'project': project, 'collected': collected, 'area_of_project': area_of_project,
                   'recommend': recommend_proj})


#MY_FAV_NUM = 15
'''def favlist(request, uid):
    try:
        user = User.objects.get(id=uid)
    except:
        return render(request, 'confirm.html', {'title': '错误', 'message': '用户不存在'})
    finally:
        proj_list = user.favorite_projects.all().order_by('pid')
        paginator = Paginator(proj_list, MY_FAV_NUM)
        page = request.GET.get('page')
        try:
            projs = paginator.page(page)
            page_num = page
        except PageNotAnInteger:
            projs = paginator.page(1)
            page_num = 1
        except EmptyPage:
            projs = paginator.page(paginator.num_pages)
            page_num = paginator.num_pages
        return render(request, 'favlist.html', {
             'user': user, })'''


def favlist(request, uid):
    #try:
        user = User.objects.get(id=uid)
        count_of_new_dynamic = 0
        level = 0
        if request.session.get('is_login'):
            current_user = User.objects.get(id=request.session.get('uid'))
            cursor = connection.cursor()
            cursor.execute(
                "select count(*) from DB4Django.Software_dynamicrecord "
                "where ((time_of_dynamic>("
                "select DB4Django.Software_userattention.time "
                "from DB4Django.Software_userattention join DB4Django.Software_project "
                "on (DB4Django.Software_userattention.follower_id = %s and DB4Django.Software_userattention.user_id = DB4Django.Software_project.creator_id) "
                "where DB4Django.Software_project.pid=DB4Django.Software_dynamicrecord.project_id) and typ=1) "
                "or time_of_dynamic>("
                "select time from DB4Django.Software_projectattention "
                "where DB4Django.Software_dynamicrecord.project_id = project_id and follower_id = %s)) "
                "and time_of_dynamic>%s",[current_user.id,current_user.id,current_user.last_view_dynamic])
            count_of_new_dynamic = cursor.fetchone()[0]
            level = current_user.level
            projects = user.favorite_projects.filter(Q(security_level__lte=level)|Q(creator_id=request.session.get('uid')))
        else:
            projects = user.favorite_projects.filter(security_level__lte=level)
            
        return render(request, 'favlist.html', {'user': user, 'count_of_new_dynamic':count_of_new_dynamic,'projects':projects})
    #except:
        return render(request, 'confirm.html', {'title': '错误', 'message': '用户不存在'})


def file_iterator(file_name, chunk_size=1024):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def file_download(request):  # 用于文件下载
    if not request.session.get('is_login'):
        return redirect('IndexV2')
    if request.method == 'GET':
        filepath = request.GET['filepath']
        filename = filepath.split('\\')[-1]
        try:
            response = StreamingHttpResponse(file_iterator(filepath))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename={0}'.format(escape_uri_path(filename))
            return response
        except:
            return render(request, 'confirm.html', {'title': '下载错误', 'message': '文件不存在'})
    else:
        return HttpResponse('method must be get')


def hash_code(s, salt='mysite'):  # 4.7
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    register_form = RegisterForm()
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        #bf = register_form._bound_fields_cache
        area = ','.join(register_form.__getitem__('area').data)
        if register_form.is_valid():  # 获取数据

            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            identity = register_form.cleaned_data['identity']
            realname = register_form.cleaned_data['realname']
            idnumber = register_form.cleaned_data['idnumber']
            sex = register_form.cleaned_data['sex']
            phone_num = register_form.cleaned_data['phone_num']
            area = ",".join(register_form.cleaned_data['area'])

            message = ''
            same_name_user = User.objects.filter(name=username)
            if same_name_user:  # 用户名唯一
                message += '用户已经存在，请重新选择用户名！\n'
            same_email_user = User.objects.filter(email=email)
            if same_email_user:  # 邮箱地址唯一
                message += '该邮箱地址已被注册，请使用别的邮箱！\n'
            if password1 != password2:  # 判断两次密码是否相同
                message += "两次输入的密码不同！\n"
            if not username.isalnum():
                message += "用户名中含有非法字符\n"
            if not (password1.isalnum() and password2.isalnum()):
                message += "密码中含有非法字符\n"
            if not idnumber.isalnum():
                message += "身份证号中含有非法字符\n"
            if not phone_num.isdigit():
                message += "电话号码中含有非法字符\n"
            if not len(username) in range(3, 17):
                message += "用户名不符合长度要求\n"
            if not (len(password1) in range(6, 17) and len(password2) in range(6, 17)):
                message += "密码不符合长度要求\n"
            if not len(idnumber) == 18:
                message += "身份证号不符合长度要求\n"
            if not len(phone_num) <= 11:
                message += "电话号码不符合长度要求\n"
            if not len(realname) < 256:
                message += "真实姓名不符合长度要求\n"
            if message != '':
                return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

            new_user = User()
            new_user.name = username
            new_user.password = hash_code(password1)  # 使用加密密码 4.7
            new_user.email = email
            new_user.sex = sex
            new_user.identity = identity
            new_user.realname = realname
            new_user.idnumber = idnumber
            new_user.phone_num = phone_num
            new_user.area = area
            new_user.last_view_dynamic = timezone.now()
            new_user.save()
            if identity == '0':
                Personal_information_entrepreneur.objects.create(user=new_user, )
            elif identity == '1':
                Personal_information_investor.objects.create(user=new_user, )

            code = make_confirm_string(new_user, 0)
            try:
                send_email(email, code)
            except:
                new_user.delete()
                return render(request, 'confirm.html', {'title': '错误', 'message': '发送确认邮件失败,请重新尝试'})
            request.session['uid'] = new_user.id
            request.session['user_name'] = new_user.name
            return render(request, 'emailverification.html', locals())

    return render(request, 'register.html', locals())


def send_email(email, code, type=0):
    from django.core.mail import EmailMultiAlternatives

    subject = '''{}'''.format(EMAIL_SUBJECT[type])

    text_content = '''\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    ip_addr = '114.115.235.135'
    if type == 4 or type == 3:
        html_content = '''
                            <p><a href="http://{}/change_password/?code={}" target=blank>{}</a>，\
                           </p>
                            <p>{}</p>
                            <p>此链接有效期为{}天！</p>
                            '''.format(ip_addr + ":8080", code, EMAIL_LINK[type], EMAIL_CONTENT[type],
                                       settings.CONFIRM_DAYS)
    else:
        html_content = '''
                        <p><a href="http://{}/confirm/?code={}" target=blank>{}</a>，\
                       </p>
                        <p>{}</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format(ip_addr + ":8080", code, EMAIL_LINK[type], EMAIL_CONTENT[type],
                                   settings.CONFIRM_DAYS)
    print(html_content)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print('mail send ok')


def make_confirm_string(user, type, content=None):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash(hash(user.name) + hash(now))
    try:
        x = ConfirmString.objects.get(user=user, type=type)
        x.code = code
    except:
        ConfirmString.objects.create(code=code, user=user, type=type)
        x = ConfirmString.objects.get(user=user, type=type)
    if type == 2 or (content != None and type == 0):
        x.new_email = content
    x.save()
    return code


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    title = '确认'
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'confirm.html', locals())

    c_time = confirm.c_time.replace(tzinfo=None)
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'confirm.html', locals())
    else:
        if confirm.type == 0:
            if confirm.new_email != None:
                confirm.user.email = confirm.new_email
            confirm.user.has_confirmed = True
            message = '感谢确认，请使用账户登录！'
        elif confirm.type == 1:
            confirm.user.has_confirmed_delete = True
            # confirm.user.d_time = timezone.now()
            confirm.user.d_time = datetime.datetime.now()
            confirm.user.save()
            Del_user.objects.create(del_user=confirm.user, del_time=now)
            message = '您的账号将在十四天后正式删除，在前七天您可以在个人中心取消这一操作'
        elif confirm.type == 2:
            confirm.user.email = confirm.new_email
            message = '您已成功修改邮箱'
        else:
            message = '错误跳转'
        confirm.user.save()
        confirm.delete()
        return render(request, 'confirm.html', locals())


# 登录
def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
            except:
                message = "用户不存在！"
                return render(request, 'login.html', locals())
            if user.password == hash_code(password):  # 4.7
                if user.has_confirmed == True:  # 第九周
                    request.session['is_login'] = True
                    request.session['uid'] = user.id
                    request.session['user_name'] = user.name
                    request.session['level'] = user.level
                    request.session['identity'] = user.identity
                    return redirect('/index/')
                else:
                    request.session['uid'] = user.id
                    request.session['user_name'] = user.name
                    message = '您尚未完成邮箱认证'
                    return render(request, 'emailverification.html', locals())
            else:
                message = "密码不正确！"
    else:
        login_form = UserForm()
    return render(request, 'login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def del_account(request):
    d_user = User.objects.get(id=request.session.get('uid'))
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    if  d_user.has_confirmed_delete:
        last_time = datetime.datetime.now() - d_user.del_user.del_time.replace(tzinfo=None)
        if request.method == 'POST':
            if (last_time < datetime.timedelta(settings.WAIT_DEL_DAYS)):
                d_user.del_user.delete()
                d_user.has_confirmed_delete = False
                d_user.save()
                message = '您已取消注销'
                return render(request, 'confirm.html', locals())
            else:
                message = '''{},{}'''.format(last_time, datetime.datetime.now())
                # message = '您注销账号已经超过七天，无法再撤销该操作'
                return render(request, 'confirm.html', locals())
        return render(request, 'wait_del_account.html', {'time': datetime.timedelta(settings.DEL_DAYS) - last_time, })
    else:
        if request.method == 'POST':
            uid = request.session.get('uid')
            user = User.objects.filter(id=uid).first()
            code = make_confirm_string(user, 1)
            send_email(user.email, code, 1)
            message = '请前往注册邮箱，进行邮件确认！'
            return render(request, 'confirm.html', locals())  # 跳转到等待邮件确认页面。
        return render(request, 'del_account.html', locals())


def wait_del_account(request):
    d_user = User.objects.get(id=request.session.get('uid'))
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    elif not d_user.has_confirmed_delete:
        return render(request, 'confirm.html', {'title': '错误', 'message': '您没有删除自己的账户'})
    last_time = datetime.datetime.now() - d_user.del_user.del_time.replace(tzinfo=None)
    if request.method == 'POST':
        if (last_time < datetime.timedelta(settings.WAIT_DEL_DAYS)):
            d_user.del_user.delete()
            d_user.has_confirmed_delete = False
            d_user.save()
            message = '您已取消注销'
            return render(request, 'confirm.html', locals())
        else:
            message = '''{},{}'''.format(last_time, datetime.datetime.now())
            # message = '您注销账号已经超过七天，无法再撤销该操作'
            return render(request, 'confirm.html', locals())
    return render(request, 'wait_del_account.html', {'time': datetime.timedelta(settings.DEL_DAYS) - last_time, })


def retrieve_pwd_send(request):
    if request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '您已经登录了'}) 
    if request.method == 'POST':
        name = request.POST['name']
        if User.objects.filter(name=name):
            user = User.objects.filter(name=name).first()
            code = make_confirm_string(user, 4)
            send_email(user.email, code, 4)
            message = '请前往注册邮箱，进行邮件确认！'
            return render(request, 'confirm.html', locals())  # 跳转到等待邮件确认页面。
        else:
            message = '用户名不存在！'
            return render(request, 'retrieve_password.html', locals())  # 跳转到等待邮件确认页面。
    return render(request, 'retrieve_password.html', locals())  # 跳转到等待邮件确认页面。


def changeemail(request):
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    if request.method == 'POST':
        new_email = request.POST['new_email']
        same_email = User.objects.filter(email=new_email)
        if same_email:
            message = '邮箱已被注册，请重新选择邮箱！'
            return render(request, 'change_email.html', locals())
        same_email = ConfirmString.objects.filter(new_email=new_email)
        if same_email:
            message = '邮箱已被注册，请重新选择邮箱！'
            return render(request, 'change_email.html', locals())
        uid = request.session.get('uid')
        user = User.objects.filter(id=uid).first()
        code = make_confirm_string(user, 2, new_email)
        send_email(user.email, code, 2)
        message = '请前往注册邮箱，进行邮件确认！'
        return render(request, 'confirm.html', locals())  # 跳转到等待邮件确认页面。
    return render(request, 'change_email.html')


def changepwd(request):
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    if request.method == 'POST':
        uid = request.session.get('uid')
        user = User.objects.filter(id=uid).first()
        code = make_confirm_string(user, 3, )
        send_email(user.email, code, 3)
        message = '请前往注册邮箱，进行邮件确认！'
        return render(request, 'confirm.html', locals())  # 跳转到等待邮件确认页面。
    return render(request, 'changepwd.html', locals())


def change_password(request):
    code = request.GET.get('code', None)
    message = ''
    title = '确认'
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'confirm.html', locals())

    c_time = confirm.c_time.replace(tzinfo=None)
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'confirm.html', locals())
    else:
        if request.method == 'POST':
            new_pwd_1 = request.POST['new_pwd_1']
            new_pwd_2 = request.POST['new_pwd_2']
            if new_pwd_1 != new_pwd_2:
                message = '两次密码不同'
                return render(request, 'change_password.html', locals())
            else:
                if len(new_pwd_1) in range(6, 17) and len(new_pwd_2) in range(6, 17):
                    if new_pwd_1.isalnum() and new_pwd_2.isalnum():
                        confirm.user.password = hash_code(new_pwd_1)
                        confirm.user.save()
                        confirm.delete()
                        message = '您已成功修改密码'
                        return render(request, 'confirm.html', locals())
                    else:
                        message = '您的输入含有非法字符'
                        return render(request, 'change_password.html', locals())
                else:
                    message = '您的输入不符合长度要求'
                    return render(request, 'change_password.html', locals())
    return render(request, 'change_password.html', locals())


def personal_information(request, uid):
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    user = User.objects.get(id=uid)
    area = [AREA_CHOICES[int(i)][1] for i in
            user.area.split(',')]
    if user.identity == 0:
        information = user.personal_information_entrepreneur
    elif user.identity == 1:
        information = user.personal_information_investor
    return render(request, "personal_information.html",
                  {'user': user, 'information': information, 'area_of_user': area})


def modify_personal_information(request,uid):
    if not request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    user = User.objects.get(id=request.session.get('uid'))
    if user.identity == 0:
        information = user.personal_information_entrepreneur
        form_info = EntrepreneurPersonalInformation(request.POST)
        form = EntrepreneurPersonalInformation(initial={'nickname': user.nickname,
                                                        'location': information.location,
                                                        'area':
                                                            [int(i) for i in
                                                             user.area.split(',')],
                                                        'introduction': user.introduction})

    elif user.identity == 1:
        information = user.personal_information_investor
        form_info = InvestorPersonalInformation(request.POST)
        form = InvestorPersonalInformation(initial={'nickname': user.nickname,
                                                    'location': information.location,
                                                    'area':
                                                        [int(i) for i in
                                                         user.area.split(',')],
                                                    'introduction': user.introduction})
    if request.method == 'POST':
        #area = ','.join(form_info.__getitem__('area').data)

        if form_info.is_valid():
            if request.FILES.get('img'):
                new_avatar = request.FILES.get('img')
                type_list = ['.jpg', '.png', '.gif', '.webp']
                # 判断上传图片格式
                if os.path.splitext(new_avatar.name)[1].lower() in type_list:
                    original_avatar = settings.MEDIA_ROOT + "\\" + user.avatar.name
                    try:
                        os.remove(original_avatar)
                    except:
                        pass
                    user.avatar = new_avatar
                    user.save()
                else:
                    return render(request, 'modify_personal_information.html',
                                  {'personal_info': form, 'type': user.identity, 'user': user})
            info = form_info.cleaned_data
            user.nickname = info['nickname']
            user.introduction = info['introduction']
            information.location = info['location']
            user.area = ",".join(info['area'])
            user.save()
            information.save()
            return render(request, 'confirm.html', {'title': '成功', 'message': '修改项目信息成功，即将跳转至主页'})
    return render(request, 'modify_personal_information.html', {'personal_info': form, 'type': user.identity, 'user': user,})


def EmailVerification(request):
    if request.session.get('is_login'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '您已经登录了'})
    if not request.session.get('uid'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请不要通过直接输网址的方式访问'})
    return render(request, 'emailverification.html', locals())

def ResendEmail(request):
    if not request.session.get('uid'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请重试'})
    if request.method == 'POST':
        uid = request.session.get('uid')
        user = User.objects.filter(id=uid).first()
        code = make_confirm_string(user, 0, user.email)
        send_email(user.email, code, 0)
        message = '请前往注册邮箱，进行邮件确认！'
        return render(request, 'confirm.html', locals())  # 跳转到等待邮件确认页面。
    return render(request, 'resendemail.html')


def ChangeAutEmail(request):
    if not request.session.get('uid'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请重试'})
    if request.method == 'POST':
        new_email = request.POST['new_email']
        same_email = User.objects.filter(email=new_email)
        if same_email:
            message = '邮箱已被注册，请重新选择邮箱！'
            return render(request, 'change_email.html', locals())
        same_email = ConfirmString.objects.filter(new_email=new_email)
        if same_email:
            message = '邮箱已被注册，请重新选择邮箱！'
            return render(request, 'change_email.html', locals())
        uid = request.session.get('uid')
        user = User.objects.filter(id=uid).first()
        code = make_confirm_string(user, 0, new_email)
        send_email(new_email, code, 0)
        message = '请前往注册邮箱，进行邮件确认！'
        return render(request, 'confirm.html', locals())  # 跳转到等待邮件确认页面。
    return render(request, 'change_email.html')

def Certification(request):
    if not request.session.get('uid'):
        return render(request, 'confirm.html', {'title': '错误', 'message': '请登录'})
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)
    message = ""
    if user.identity == 0:
        return render(request, 'confirm.html', {'title': '错误', 'message': '您不是投资人'})
    try:
        information = user.applicant
        form = ApplicationForm(initial={'company': information.company,
                                        'position': information.position,
                                        'scale': information.scale,
                                        'currency': information.currency,
                                        'introduction': information.introduction})
    except:
        form = ApplicationForm()
    if request.method == "POST":
        application_form = ApplicationForm(request.POST)
        message = "请检查填写的内容！"
        if application_form.is_valid():
            company = application_form.cleaned_data['company']
            position = application_form.cleaned_data['position']
            scale = application_form.cleaned_data['scale']
            currency = application_form.cleaned_data['currency']
            introduction = application_form.cleaned_data['introduction']
            try:
                new_applicant = Applicant.objects.get(user_id=uid)
            except:
                new_applicant = Applicant()
                new_applicant.user_id = uid            
            new_applicant.company = company
            new_applicant.position = position
            new_applicant.scale = scale
            new_applicant.currency = currency
            new_applicant.introduction = introduction
            new_applicant.save()
            return render(request, 'confirm.html', {'title': '成功', 'message': '后台正在为您人工审核'})
    return render(request, 'certification.html', {'user':user,'application_form': form, 'message': message})

from haystack.views import SearchView
class MySearchView(SearchView):

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        level = 0
        if request.session.get('is_login'):
            level = User.objects.get(id=request.session.get('uid')).level
            self.results = self.get_results().filter(Q(security__lte=level)|Q(creator_id=request.session.get('uid')))
        else:
            self.results = self.get_results().filter(security__lte=level)
        return self.create_response()


def ajax_captcha(request):  # 验证码输入验证
    if request.is_ajax():
        result = CaptchaStore.objects.filter(response=request.GET.get('response'), hashkey=request.GET.get('hashkey'))
        if result:
            data = {'status': 1}
        else:
            data = {'status': 0}
        return JsonResponse(data)
