from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from pages import views


urlpatterns = [
    path('', views.HomeView.as_view()),

    path('sitemap.xml', views.sitemap),
    path('robots.txt', views.robots),
    path('feedback/', views.feedback),
    path('resolution/<slug:key>/', views.resolution, name='resolution'),
    path('test', views.test),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('myadmin/', admin.site.urls),
    path('myadmin/cache/clear/<int:pk>/', views.admin_clear_cache, name='clear_cache'),
]

# DEBUG TOOLBAR
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += [path('<path:slug>', views.PageView.as_view(), name='page')]
