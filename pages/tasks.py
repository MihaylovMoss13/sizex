# -*- coding:utf-8 -*-

import logging
import os
import zlib
import requests
import redis
import htmlmin

from celery import task
from django.conf import settings
from pages.models import Pages
from django.template.loader import render_to_string
from telegram_send import send

logger = logging.getLogger(__name__)

DESKTOP_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
MOBILE_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'

rds = redis.Redis(**settings.CACHE_REDIS)
CACHE_TTL = 60 * 60 * 24 * 30
TIMEOUT = 10


@task()
def offload(host, path, resolution):
    # TODO: need move 'room-potolok' to settings
    if 'room-potolok' not in host:
        return

    key = 'cache:' + host + path + resolution
    headers = {
        'Offload': 'true',
        'User-Agent': DESKTOP_AGENT
    }

    if resolution == 'mobile':
        headers['User-Agent'] = MOBILE_AGENT

    resp = requests.get('http://' + host + path, headers=headers, timeout=TIMEOUT)
    if resp.status_code == 200:
        rds.set(key, zlib.compress(htmlmin.minify(resp.text).encode('utf8')), CACHE_TTL)


@task()
def tsend(messages):
    send(messages=messages, parse_mode='html', conf='/etc/telegram/telegram.conf')


@task()
def set_active():
    from pages.models import Pages
    if Pages.objects.filter(level=3, status=False).count() > 0:
        messages = ['Добавлены новые страницы:']
        for p in Pages.objects.filter(level=3, status=False)[:7]:
            logger.info('Add page: ' + p.get_absolute_url())
            messages.append(p.get_absolute_url())
            p.status = True
            p.save()
        send(messages=messages, parse_mode='html', conf='/etc/telegram/telegram2.conf')

@task
def create_rss():
    tree_ids = [p.tree_id for p in Pages.objects.filter(name__in=[
        'Верхнее меню',
        'Верхнее меню2',
        'Каталог'
    ])]
    pages = Pages.objects.filter(tree_id__in=tree_ids, status=True)
    path = os.path.join(settings.STATIC_ROOT, 'rss.html')
    print(path)
    with open(path, 'w') as fn:
        fn.write(render_to_string('rss.html', {'pages': pages}))
