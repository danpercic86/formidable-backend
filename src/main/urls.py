from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from dj_rest_auth.views import PasswordResetConfirmView
from django.views.generic import TemplateView

from formidable.urls import common_urls


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='admin:index', permanent=True)),
    path('api/admin/docs/', include('django.contrib.admindocs.urls'), name='docs'),
    path('api/admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/', include(common_urls)),
    path('api/i18n/', include('django.conf.urls.i18n')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then allauth by defaul redirects
    # to a view to tell you need to confirm email.
    path('dummy/', TemplateView.as_view(), name='account_email_verification_sent'),
    path(
        'api/auth/password/reset/confirm/<slug:uidb64>/<slug:token>/',
        TemplateView.as_view(),
        name='password_reset_confirm',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('api/__debug__/', include(debug_toolbar.urls), name='debug')]
