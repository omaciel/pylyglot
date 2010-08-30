# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai
#
# This file is part of Pylyglot.
#
# Pylyglot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylyglot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pylyglot.  If not, see <http://www.gnu.org/licenses/>.

from core.views import *
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('pylyglot.translations.urls')),
    url(r'^rpc_service/$', include('pylyglot.rpc_service.urls')),

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
