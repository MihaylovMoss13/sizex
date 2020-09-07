# -*- coding:utf-8 -*-

import os
import re
import time

from email.utils import formatdate
from django.conf import settings

from pages.changer import changer


def change_name(string):
    alias = ''
    for item in string.lower():
        if item in changer:
            alias += changer[item]
        else:
            alias += item
    alias = re.sub(u'[^A-Za-z0-9-_\/\.\s]+', '', alias)
    alias = re.sub(u'-{2,10}', '-', alias)
    alias = alias.replace(' ', '-')
    return alias


def update_filename(instance, filename):
    path = instance.folder
    fn = change_name(instance.name)
    return os.path.join(path, fn + '.' + filename.split('.')[-1])


def get_template(request, template):
    if request.session.get(settings.RESOLUTION_KEY) == 'mobile':
        # hack for version without mobile layout
        return template + '_mobile.html'
    # return template + '_mobile.html'
    return template + '.html'


def datetime2rfc(dt):
    dt = time.mktime(dt.timetuple())
    return formatdate(dt, usegmt=True)
