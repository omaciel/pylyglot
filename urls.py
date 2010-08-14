from aurelio.views import *
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^bidu/', include('bidu.foo.urls')),

    url(r'^$', front_page, name="frontpage"),
    url(r'^packages/', packages_page, name="packages"),
    url(r'^translations/', translations_page, name="translations"),

    # Administration
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
