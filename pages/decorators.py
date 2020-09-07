# -*- coding:utf-8 -*-

from django.http import Http404


def domain(host):
    def fabric(func):
        def wrapped(request, *args, **kwargs):
            if request.get_host() != host:
                raise Http404
            return func(request, *args, **kwargs)
        return wrapped
    return fabric
