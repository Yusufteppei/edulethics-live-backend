from django.contrib import admin
from django.urls import path, include

from exam.admin_views import menu


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", menu, name='index'),
    path('admin/clearcache/', include('clearcache.urls')),

    path("admin/", admin.site.urls, name='admin'),
    path("exam/", include("exam.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("authentication.urls")),
    #path('summernote/', include('django_summernote.urls')),
    path('chat/', include('chat.urls')),
    path('notification/', include('notification.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
