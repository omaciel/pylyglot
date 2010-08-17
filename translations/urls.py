from django.conf.urls.defaults import *

urlpatterns = patterns('bidu.translations.views',

        url(r'^$', 'index', name='translations_list'),
)
