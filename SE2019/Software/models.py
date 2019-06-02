from django.db import models
from .GlobalVariable import *
from django.utils import timezone
import random
import string
from imagekit.models import ProcessedImageField  # 头像
from imagekit.processors import ResizeToFill

# Create your models here.
#
class Project(models.Model):
    pid = models.AutoField(primary_key=True, )
    name = models.CharField(max_length=100, verbose_name='项目名称')
    creator = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='项目创建者',
        related_name='my_project',
    )
    company_name = models.CharField(max_length=50, default='', verbose_name='企业名称', blank=True)
    area = models.CharField(max_length=1000, verbose_name='项目领域')
    introduction = models.CharField(max_length=200, verbose_name='项目简介')
    detailed_introduction = models.TextField(verbose_name='项目详细介绍', default='', blank=True)
    location = models.CharField(max_length=50, verbose_name='地区')
    proposal = models.FileField(upload_to='uploads/%Y/%m/%d', verbose_name="商业策划书", null=True, blank=True)
    recruit = models.BooleanField(default=False, verbose_name='项目招聘状态')
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name='项目进展状态', default=0)
    security_level = models.IntegerField(choices=SECURITY_LEVEL_CHOICES, verbose_name='项目保密等级', default=0)
    favorite_projects = models.ManyToManyField(
        'User',
        verbose_name='收藏的项目',
        through='ProjectAttention',
        related_name='favorite_projects'
    )
    additional_documents = models.FileField(upload_to='uploads/additional/%Y/%m/%d', verbose_name='附加材料', null=True, blank=True)
    time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    avatar = ProcessedImageField(upload_to='uploaded',
                                 processors=[ResizeToFill(64, 64)],
                                 format='JPEG',
                                 options={'quality': 60},
                                 default="uploaded/noface.gif",
                                 )
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    realname = models.CharField(max_length=256)
    idnumber = models.CharField(max_length=256)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    identity = models.IntegerField(choices=category, default=0)
    c_time = models.DateTimeField(auto_now_add=True)
    d_time = models.DateTimeField(null=True, default=None, blank=True)
    has_confirmed = models.BooleanField(default=False)
    has_confirmed_delete = models.BooleanField(default=False)  # 4.7
    last_view_dynamic = models.DateTimeField()
    follower = models.ManyToManyField(
        'self',
        verbose_name='关注者',
        through='UserAttention',
        symmetrical=False,
        related_name='follower_of_user',
    )
    history = models.ManyToManyField(
        'Project',
        verbose_name='浏览历史',
        through='History',
        related_name='history',
    )
    phone_num = models.CharField(max_length=20)
    introduction = models.TextField(max_length=1000, default="尚待补充", verbose_name="简介")
    nickname = models.CharField(max_length=10, default=''.join(random.sample(string.ascii_letters + string.digits, 8)))
    area = models.CharField(max_length=1000, verbose_name='关注领域')
    level = models.IntegerField(default=0)#用户等级 0:普通用户 1:小投资人 2:大投资人
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)
    new_password = models.CharField(max_length=256, null=True)
    new_email = models.EmailField(null=True)
    type = models.IntegerField(null=True)

    # d_time = models.DateTimeField(default=timezone.now)  # 4.7
    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
        unique_together = ('user', 'type')


class History(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='myhistory'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        verbose_name='项目',
        related_name='+'
    )
    time = models.DateTimeField(verbose_name='浏览日期', auto_now=True)

    class Meta:
        unique_together = ('user', 'project')
        ordering = ["-time"]


class UserAttention(models.Model):  # 用户关注
    follower = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='关注者',
        related_name='+',
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='用户(被关注者)',
        related_name='+',
    )
    time = models.DateTimeField(verbose_name='关注时间', auto_now=True)

    class Meta:
        unique_together = ('follower', 'user')


class ProjectAttention(models.Model):  # 项目收藏
    follower = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='关注者',
        related_name='+',
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        verbose_name='被关注项目',
        related_name='+',
    )
    time = models.DateTimeField(verbose_name='关注时间', auto_now=True)

    class Meta:
        unique_together = ('follower', 'project')


class DynamicRecord(models.Model):  # 动态
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="dynamic_of_this"
    )
    typ = models.IntegerField()  # 0:项目动态（信息修改） 1:用户动态（项目新建） 2：用户动态（项目修改）
    time_of_dynamic = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_of_dynamic"]


class Del_user(models.Model):
    del_time = models.DateTimeField(auto_now_add=True)
    del_user = models.OneToOneField('User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['del_time']


class Personal_information_investor(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    location = models.CharField(max_length=128, null=True)


class Personal_information_entrepreneur(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    location = models.CharField(max_length=128, null=True)


class Applicant(models.Model):
    user = models.OneToOneField("User",on_delete=models.CASCADE,related_name="applicant",verbose_name="申请用户")
    company = models.CharField(max_length=100, verbose_name='所属公司')
    position = models.CharField(max_length=100, verbose_name='职位')
    scale = models.CharField(max_length=100, verbose_name='投资规模')
    currency = models.CharField(max_length=100, verbose_name='投资币种')
    introduction = models.TextField(max_length=10000, verbose_name='简介')
    def __str__(self):
        return self.user.name
