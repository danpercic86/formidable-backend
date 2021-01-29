from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from formidable.urls import common_urls

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='admin:index', permanent=True)),
    path('api/admin/docs/', include('django.contrib.admindocs.urls'), name='docs'),
    path('api/admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/', include(common_urls)),
    path('api/i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('api/__debug__/', include(debug_toolbar.urls), name='debug')]
