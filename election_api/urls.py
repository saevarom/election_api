from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls

from core import urls as overcast_urls

from api import urls as api_urls

from wagtail.wagtailsearch.signal_handlers import register_signal_handlers as wagtailsearch_register_signal_handlers
wagtailsearch_register_signal_handlers()

urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/', include(wagtailsearch_frontend_urls)),

    url(r'^test404/$', TemplateView.as_view(template_name="404.html")),
    url(r'^test500/$', TemplateView.as_view(template_name="500.html")),


    url(r'^api/', include(api_urls)),

    url(r'', include(overcast_urls)),

    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'overcast/images/favicon.ico'))
    ]

    handler404 = 'core.views.error404'
