import pickle, os, sys
parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_path)
print(parent_path)
os.environ.update({"DJANGO_SETTINGS_MODULE": "Django.settings"})
# setup_environ(settings)
import django
django.setup()
from Software.models import Project, User, DynamicRecord
from Software.GlobalVariable import *
import random

def field2int(f):
    for e in AREA_CHOICES:
        if e[-1] == f:
            return e[0]
    raise ValueError('missed field')


def phase2int(ph):
    for e in STATUS_CHOICES:
        if e[-1] == ph:
            return e[0]
    raise ValueError('missed phase')

projects = pickle.load(open('../RecommendSys/washed1_pro.pk', 'rb'))
for i,e in enumerate(projects):
    try:
        c = Project.objects.filter(name=e[0], location=e[4], status=phase2int(e[1]))
        if len(c)!=0:
            if len(c) != 1:
                print(c)
            continue
        if (e[1] == '未融资' and random.random() > 0.02) or (e[1] != '未融资' and random.random() > 0.08):
            continue
        project = Project()
        project.name = e[0]
        project.company_name = e[0]
        area = e[2].split(',')
        b = []
        for a in area:
            b.append(str(field2int(a)))
        project.area = ",".join(b)
        project.introduction = e[0]
        project.detailed_introduction = e[5]
        project.location = e[4]
        # project.proposal = info['proposal']
        project.creator = User.objects.get(id=1)
        # project.creator = User.objects.get(id=1)  # for test
        # project.recruit = info['recruit']
        project.security_level = 0
        project.status = phase2int(e[1])
        project.save()
        DynamicRecord.objects.create(project=project, typ=1)
    except Exception as e:
        print(e)
        print(i)
