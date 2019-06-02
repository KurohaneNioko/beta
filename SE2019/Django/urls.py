"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Software import views as software_view
from django.conf.urls import include
from django.views.static import serve
from django.conf import settings

urlpatterns = (
    path('index/', software_view.index, name='IndexV2'),
    path('space/<int:uid>', software_view.space, name='Space'),
    path('space/<int:uid>/favlist', software_view.favlist, name='Favlist'),
    path('space/<int:uid>/my_projects', software_view.my_projects, name='MyProject'),
    path('space/<int:uid>/fans', software_view.fans, name='Fans'),
    path('space/<int:uid>/follow', software_view.follow, name='Follow'),
    path('register/', software_view.register, name='Register'),
    path('login/', software_view.login, name='Login'),
    path('logout/', software_view.logout, name='Logout'),
    path('confirm/', software_view.user_confirm, name='Confirm'),
    path('captcha/', include('captcha.urls')),
    path('ReleaseProject/', software_view.release_project, name='ReleaseProject'),
    path('history/', software_view.history, name='History'),
    path('project_list/', software_view.project_list, name='ProjectList'),
    path('project_info/<int:pid>', software_view.project_info, name='ProjectInfo'),
    path("ModifyProject/<int:pid>", software_view.modify_project, name='ModifyProject'),
    path('dynamic/', software_view.dynamic, name='Dynamic'),
    path('', include("message.urls")),
    path('del_account/', software_view.del_account, name='Del_account'),
    path('wait_del_account/', software_view.wait_del_account, name='Wait_del_account'),
    path('change_email/', software_view.changeemail, name='Change_email'),
    path('change_password/', software_view.change_password, name='Change_password'),
    path('changepwd/', software_view.changepwd, name='Changepwd'),
    path('retrieve_password/', software_view.retrieve_pwd_send, name='Retrieve_password'),
    path('personal_information/<int:uid>', software_view.personal_information, name='Personal_information'),
    path('modify_personal_information/<int:uid>', software_view.modify_personal_information,
         name='Modify_personal_information'),
    path('download/', software_view.file_download),

    # path('search/', include('haystack.urls')),
    path('search/', software_view.MySearchView(), name='haystack_search'),
    path('admin/', admin.site.urls),
    path('emailverification/', software_view.EmailVerification, name='Emailverification'),
    path('resendemail/', software_view.ResendEmail, name='Resendemail'),
    path('changeautemail/', software_view.ChangeAutEmail, name='Changeautemail'),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    #path('favicon.ico', serve, {'path': 'static/favicon.ico'}),
    path('certification/', software_view.Certification, name='Certification'),
    path('ajax_captcha/', software_view.ajax_captcha, name='ajax_captcha'),
    path('captcha/', include('captcha.urls')),
)
