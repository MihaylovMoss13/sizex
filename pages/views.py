import redis

from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from rest_framework.parsers import JSONParser

from .models import Pages, Domain, IndexBlock
from .tasks import tsend
# from .decorators import domain
from .serializers import FeedbackSerializer
from .utils import get_template
from django.contrib.auth.decorators import user_passes_test


class HomeView(DetailView):
    def get(self, *args, **kwargs):
        self.page = Pages.objects.filter(domain__domain=self.request.get_host(), alias='').first()
        if not self.page:
            raise Http404
        return render(
            self.request,
            get_template(self.request, self.page.template or 'index'),
            {'obj': self.page, 'object': self.page, 'iblocks': IndexBlock.objects.filter(status=True)}
        )


class PageView(DetailView):
    model = Pages
    slug_field = 'alias'

    def get(self, *args, **kwargs):
        self.slug = kwargs.get('slug')

        # Получаем страницу
        self.page = Pages.objects.filter(alias=self.slug, domain__domain=self.request.get_host(), status=True).first()
        if self.page:
            return render(
                self.request,
                get_template(self.request, self.page.template or 'pages/pages_detail'),
                {
                    'object': self.page,
                    'blocks': self.page.pagesblock_set.all(),
                }
            )

        raise Http404


def sitemap(request):
    urls = []

    # Add pages
    [urls.append({
        'url': page.get_absolute_url(),
        'freq': 'daily',
        'priority': '0.8'
    }) for page in Pages.objects.filter(status=True, domain__domain=request.get_host()).order_by('lft')]

    response = render(request, 'sitemap.xml', {'urls': urls, 'domain': request.get_host()})
    response['Content-type'] = 'text/xml'
    return response


def robots(request):
    response = render(request, 'robots.txt', {'domain': request.get_host()})
    response['Content-type'] = 'text/plain; charset=UTF-8'
    return response


def resolution(request, key):
    request.session[settings.RESOLUTION_KEY] = key
    referer = request.META.get('HTTP_REFERER') or '/'
    return HttpResponseRedirect(referer)


def test(request):
    if settings.DEBUG:
        return render(request, get_template(request, 'test'), {})
    raise Http404


@csrf_exempt
def feedback(request):
    data = JSONParser().parse(request)
    serializer = FeedbackSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        domain = Domain.objects.first()
        messages = [
            '<a href="http://%s/myadmin/pages/feedback/%d/change/">Новая заявка</a>' % (domain.domain, serializer.data['id'])
        ]
        tsend.delay(messages)
        return JsonResponse({'success': True, 'data': serializer.data})
    else:
        return JsonResponse({'success': False, 'errors': serializer.errors})


@user_passes_test(lambda u: u.is_superuser)
def admin_clear_cache(request, pk):
    instance = Pages.objects.get(id=pk)
    rds = redis.Redis(**settings.CACHE_REDIS)
    url = instance.get_absolute_url().replace('http://', '')
    url = url + '/' if url[-1] != '/' else url
    key = 'cache:%sdesktop' % url
    rds.delete(key)
    key = 'cache:%smobile' % url
    rds.delete(key)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/myadmin/')
