from django import forms
from .GlobalVariable import *
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    category = (
        (1, "投资人"),
        (0, "非投资人"),
    )
    username = forms.CharField(label="用户名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=32,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", max_length=32, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    realname = forms.CharField(label="真实姓名", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    idnumber = forms.CharField(label="身份证号", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    identity = forms.ChoiceField(label='身份', choices=category)
    sex = forms.ChoiceField(label='性别', choices=gender)
    area = forms.MultipleChoiceField(label='您关注的领域', widget=forms.CheckboxSelectMultiple, choices=AREA_CHOICES,error_messages={'required': '请填写项目领域','invalid':"请正确填写项目领域"})
    captcha = CaptchaField(label='验证码',error_messages={'required': '请填写验证码','invalid':"请正确填写验证码"})
    phone_num = forms.CharField(label="手机号", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))


class Form4ProjectRelease(forms.Form):
    name = forms.CharField(max_length=100, label="项目名称", required=True,error_messages={'required': '请填写项目名称','invalid':"请正确填写项目名称"})
    company = forms.CharField(max_length=50, label="公司名称", required=False,error_messages={'invalid':"请正确填写公司名称"})
    area = forms.MultipleChoiceField(choices=AREA_CHOICES, label="项目领域",
                                     widget=forms.CheckboxSelectMultiple,error_messages={'required': '请填写项目领域','invalid':"请正确填写项目领域"})
    introduction = forms.CharField(max_length=200, label="项目简介", required=True, widget=forms.Textarea,error_messages={'required': '请填写项目简介','invalid':"请正确填写项目简介"})
    detailed_introduction = forms.CharField(label="项目详细介绍", required=False, widget=forms.Textarea,error_messages={'invalid':"请正确填写项目详细介绍"})
    # province = forms.ChoiceField(choices=PROVINCE_CHOICES, required=True, label='所在省')
    # city = forms.ChoiceField(choices=CITY_CHOICES.get(province), required=True, label="所在市")
    location = forms.CharField(max_length=50, label='地区',error_messages={'required': '请填写地区','invalid':"请正确填写地区"})
    proposal = forms.FileField(label='商业策划书', required=False,error_messages={'invalid':"请正确上传不大于10mb的文件"})
    recruit = forms.ChoiceField(choices=((True, "需要招聘"), (False, "不需要招聘")), required=True, label='项目招聘状态',
                                widget=forms.RadioSelect, initial=False,error_messages={'required': '请填写项目是否招聘','invalid':"请正确填写项目招聘状态"})
    status = forms.ChoiceField(choices=STATUS_CHOICES[2:], required=True, label="项目融资状态",error_messages={'required': '请填写项目融资状态','invalid':"请正确填写项目融资状态"})
    security_level = forms.ChoiceField(choices=SECURITY_LEVEL_CHOICES, required=True, label="项目保密等级",error_messages={'required': '请填写项目保密等级','invalid':"请正确填写项目保密等级"})
    captcha = CaptchaField(label='验证码',error_messages={'required': '请填写验证码','invalid':"请正确填写验证码"})

class Form4ProjectModify(forms.Form):
    company = forms.CharField(max_length=50, label="公司名称", required=False,error_messages={'invalid':"请正确填写公司名称"})
    area = forms.MultipleChoiceField(choices=AREA_CHOICES, label="项目领域",
                                     widget=forms.CheckboxSelectMultiple,error_messages={'required': '请填写项目领域','invalid':"请正确填写项目领域"})
    introduction = forms.CharField(max_length=200, label="项目简介", required=True, widget=forms.Textarea,error_messages={'required': '请填写项目简介','invalid':"请正确填写项目简介"})
    detailed_introduction = forms.CharField(label="项目详细介绍", required=False, widget=forms.Textarea,error_messages={'invalid':"请正确填写项目详细介绍"})
    # province = forms.ChoiceField(choices=PROVINCE_CHOICES, required=True, label='所在省')
    # city = forms.ChoiceField(choices=CITY_CHOICES.get(province), required=True, label="所在市")
    location = forms.CharField(max_length=50, label='地区',error_messages={'required': '请填写地区','invalid':"请正确填写地区"})
    proposal = forms.FileField(label='商业策划书', required=False,error_messages={'invalid':"请正确上传不大于10mb的文件"})
    recruit = forms.ChoiceField(choices=((True, "需要招聘"), (False, "不需要招聘")), required=True, label='项目招聘状态',
                                widget=forms.RadioSelect, initial=False,error_messages={'required': '请填写项目是否招聘','invalid':"请正确填写项目招聘状态"})
    status = forms.ChoiceField(choices=STATUS_CHOICES[2:], required=True, label="项目融资状态",error_messages={'required': '请填写项目融资状态','invalid':"请正确填写项目融资状态"})
    security_level = forms.ChoiceField(choices=SECURITY_LEVEL_CHOICES, required=True, label="项目保密等级",error_messages={'required': '请填写项目保密等级','invalid':"请正确填写项目保密等级"})
    captcha = CaptchaField(label='验证码',error_messages={'required': '请填写验证码','invalid':"请正确填写验证码"})
    '''company = forms.CharField(max_length=50, label="公司名称", required=False)
    area = forms.MultipleChoiceField(choices=AREA_CHOICES, required=True, label="项目领域",
                                     widget=forms.CheckboxSelectMultiple,error_messages={'required': '请填写项目领域'})
    introduction = forms.CharField(max_length=200, label="项目简介", required=True, widget=forms.Textarea,error_messages={'required': '请填写项目简介'})
    detailed_introduction = forms.CharField(label="项目详细介绍", required=False, widget=forms.Textarea)
    # province = forms.ChoiceField(choices=PROVINCE_CHOICES, required=True, label='所在省')
    # city = forms.ChoiceField(choices=CITY_CHOICES.get(province), required=True, label="所在市")
    location = forms.CharField(max_length=50, label='地区', required=True,error_messages={'required': '请填写地区'})
    proposal = forms.FileField(label='商业策划书', required=False)
    recruit = forms.ChoiceField(choices=((True, "需要招聘"), (False, "不需要招聘")), required=True, label='项目招聘状态',
                                widget=forms.RadioSelect, initial=False,error_messages={'required': '请填写项目招聘状态'})
    status = forms.ChoiceField(choices=STATUS_CHOICES[1:], required=True, label="项目融资状态",error_messages={'required': '请填写项目融资状态'})
    security_level = forms.ChoiceField(choices=SECURITY_LEVEL_CHOICES, required=True, label="项目保密等级",error_messages={'required': '请填写项目保密等级'})
    captcha = CaptchaField(label='验证码',error_messages={'required': '请填写验证码'})'''


class InvestorPersonalInformation(forms.Form):
    nickname = forms.CharField(max_length=100, label="昵称", required=True)
    location = forms.CharField(max_length=100, label="位置", required=False)
    introduction = forms.CharField(max_length=1000, label="个人简介", required=False, widget=forms.Textarea)
    area = forms.MultipleChoiceField(label='您关注的领域', widget=forms.CheckboxSelectMultiple, choices=AREA_CHOICES,error_messages={'required': '请填写项目领域','invalid':"请正确填写项目领域"})


class EntrepreneurPersonalInformation(forms.Form):
    nickname = forms.CharField(max_length=100, label="昵称", required=False)
    location = forms.CharField(max_length=100, label="位置", required=False)
    introduction = forms.CharField(max_length=1000, label="个人简介", required=False, widget=forms.Textarea)
    area = forms.MultipleChoiceField(label='您关注的领域', widget=forms.CheckboxSelectMultiple, choices=AREA_CHOICES,error_messages={'required': '请填写项目领域','invalid':"请正确填写项目领域"})


class ApplicationForm(forms.Form):
    company = forms.CharField(max_length=100, label='*所属公司（可以为个人）', required=True)
    position = forms.CharField(max_length=100, label='职位', required=False)
    scale = forms.CharField(max_length=100, label='*投资规模', required=True)
    currency = forms.CharField(max_length=100, label='*投资币种', required=True)
    introduction = forms.CharField(max_length=10000, label='*简介', required=True, widget=forms.Textarea)

