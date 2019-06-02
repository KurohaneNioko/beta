from ..GlobalVariable import *
from django import template

register = template.Library()


@register.filter
def status2str(value):
    """把template中的status数字转换成内容"""
    for e in STATUS_CHOICES:
        if e[0] == int(value):
            return e[1]
    return "!Null_Status!"


@register.filter
def area2list(value):
    """把template中的area+逗号转换成内容"""
    value = value.split(',')
    s = []
    for i in value:
        for a in AREA_CHOICES:
            if int(i) == a[0]:
                s.append(a[1])
    return s


@register.filter
def getAREA_CHOICE(value):
    """直接变换成AREA_CHOICES"""
    return AREA_CHOICES


@register.filter
def area2zhcn(value):
    """借助forloop.counter0，得到领域名称"""
    return AREA_CHOICES[int(value)][1]


@register.filter
def chk_num_list(value):
    """把Project的领域转成数字做的list"""
    return list(map(lambda x:int(x), value.split(',')))


@register.filter
def recommend_cut(value, arg):
    """限制推荐部分的文字长度"""
    return value+(' '*(int(arg)+3-len(value))) if len(value) <= int(arg) else value[:int(arg)]+'...'

@register.filter
def is_even(value):
    """偶数判断"""
    return (int(value)) & 1 == 0


@register.filter
def permission_select(value,level):
    #选择出符合权限要求的项目
    return value.filter(security_level__lte=level)

@register.filter
def permission_select_search(value,level):
    #选择出符合权限要求的项目
    return value


@register.filter
def checkbox_arealist(value):
    """把arealist转换成数字组成的list"""
    value = value.split(',')
    s = list(map(int, value))
    return s


class SetVarNode(template.Node):


    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value


    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


'''def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])'''
class VarAddOneNode(template.Node):
 
    def __init__(self, var_name):
        self.var_name = var_name
 
    def render(self, context):
        try:
            value = template.Variable(self.var_name).resolve(context)
            context[self.var_name] = str( int(value) + 1 )
        except template.VariableDoesNotExist:
            value = ""
 
        return u""
 
def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) == 2:
        content = parts[1]
        if content[len(content)-2 :len(content)] == '++':
            var_name = content[:len(content) - 2]
            return VarAddOneNode(var_name)
        else:
            return u""
    elif len(parts) == 4:
        return SetVarNode(parts[1], parts[3])


register.tag('set', set_var)
