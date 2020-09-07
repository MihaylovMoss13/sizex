# -*- coding:utf-8 -*-

import redis
import zlib
import re

from logging import getLogger

from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.conf import settings
from .models import Redirect
from .tasks import offload, CACHE_TTL

logger = getLogger(__name__)
rds = redis.Redis(**settings.CACHE_REDIS)
CACHE_TTL_FUCKUP = 60 * 60

IGNORE_URLS = [
    'rss',
    'robots.txt',
    'sitemap.xml',
    'resolution',
    'feedback',
    'search',
    'ckeditor',
    'jet',
    'myadmin',
    'static',
    'media'
]

EXPRESSION = re.compile(r'^/({}).*'.format('|'.join(IGNORE_URLS)))


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect = Redirect.objects.filter(fr=request.path, domain__domain=request.get_host()).first()
        if redirect:
            if redirect.code == '0':
                return HttpResponsePermanentRedirect(redirect.to)
            elif redirect.code == '1':
                return HttpResponseRedirect(redirect.to)
        response = self.get_response(request)
        return response


class MobileMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if settings.RESOLUTION_KEY not in request.session:
                if settings.USER_AGENTS.match(request.META.get('HTTP_USER_AGENT')):
                    request.session[settings.RESOLUTION_KEY] = 'mobile'
                else:
                    request.session[settings.RESOLUTION_KEY] = 'desktop'
        except TypeError:
            request.session[settings.RESOLUTION_KEY] = 'desktop'

        logger.info('Resolution: %s' % request.session[settings.RESOLUTION_KEY])

        if not EXPRESSION.match(request.get_full_path()) and 'HTTP_OFFLOAD' not in request.META and 'HTTP_HOST' in request.META:
            key = 'cache:' + request.META['HTTP_HOST'] + request.get_full_path() + request.session[settings.RESOLUTION_KEY]
            logger.info(key)
            if not rds.keys(key) or rds.ttl(key) < CACHE_TTL - CACHE_TTL_FUCKUP:
                offload.delay(request.META['HTTP_HOST'], request.get_full_path(), request.session[settings.RESOLUTION_KEY])
            if rds.keys(key):
                logger.info('Response from redis')
                content = zlib.decompress(rds.get(key))
                return HttpResponse(content)

        response = self.get_response(request)

        if hasattr(request, 'session'):
            if request.COOKIES.get(settings.RESOLUTION_KEY) != request.session.get(settings.RESOLUTION_KEY):
                logger.info('Set resolution cookie')
                response.set_cookie(settings.RESOLUTION_KEY, request.session.get(settings.RESOLUTION_KEY))

            if 'HTTP_OFFLOAD' in request.META:
                response.content = response.content.decode('utf8')

        logger.info('Response from app')
        return response


class VaryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Vary'] = 'User-Agent'
        logger.info('Set vary header')
        return response
