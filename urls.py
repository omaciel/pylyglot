from core.views import *
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('bidu.translations.urls')),

    # Administration
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.generic.simple',
        url(r'^about', 'direct_to_template', {'template': 'about.html'}, name='about'),
        url(r'^howto', 'direct_to_template', {'template': 'howto.html'}, name='howto'),
        url(r'^contact', 'direct_to_template', {'template': 'contact.html'}, name='contact'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT},
            name='media',
        ),
    )
