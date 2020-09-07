# -*- coding:utf-8 -*-

import datetime

from pages.models import Pages, Domain
from django.utils import translation
from django.conf import settings


def app(request):
    context = {
        'DEBUG': settings.DEBUG,
        'YEAR': datetime.date.today().year,
        'CDN_DOMAIN': settings.CDN_DOMAIN,
        'CONTACTS': settings.CONTACTS,
        'TOWNS': Domain.objects.order_by('id').all(),
        'DOMAIN': Domain.objects.filter(domain=request.get_host()).first()
    }

    try:
        top_menu = Pages.objects.filter(name='Верхнее меню').first()
        if top_menu:
            context.update({'top_menu': top_menu.get_children().filter(status=True)})
    except Pages.DoesNotExist:
        pass

    try:
        subtop_menu = Pages.objects.filter(name='Верхнее меню2').first()
        if subtop_menu:
            context.update({'subtop_menu': subtop_menu.get_children().filter(status=True)})
    except Pages.DoesNotExist:
        pass

    try:
        left_menu = Pages.objects.filter(name='Каталог').first()
        if left_menu:
            context.update({'left_menu': left_menu.get_children().filter(status=True)})
    except Pages.DoesNotExist:
        pass

    return context
