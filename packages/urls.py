from django.conf.urls.defaults import *

urlpatterns = patterns('bidu.packages.views',

        url(r'^$', 'index', name='packages_list'),
        url(r'^(?P<object_id>\d+)/$', 'detail', name='package_detail'),
)
