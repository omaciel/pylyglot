# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *
from aurelio.views import *

urlpatterns = patterns('',
    # Browsing
    url(r'^$', glossary_page, name='glossary_glossary_list'),
    url(r'^packages', packages_page, name='packages_list'),
)

