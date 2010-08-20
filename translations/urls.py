from django.conf.urls.defaults import *

urlpatterns = patterns('pylyglot.translations.views',

        url(r'^$', 'index', name='home'),
)
