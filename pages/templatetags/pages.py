# -*- coding:utf-8 -*-

from django.template import Library, Template, Context

register = Library()

@register.simple_tag
def verbose_name(instance, field_name):
    """ Returns verbose_name for a field.  """
    return instance._meta.get_field(field_name).verbose_name.title()


@register.filter(name='cut')
def cut(value, arg=30):
    if len(value) > arg:
        return value[:arg] + '...'
    else:
        return value
