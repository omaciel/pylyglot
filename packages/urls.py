from django.conf.urls.defaults import *
from bidu.aurelio.models import Package

info_dict = {
    'queryset': Package.objects.all(),
}

urlpatterns = patterns('',

    (r'^$', 'django.views.generic.list_detail.object_list', info_dict, 'package_list'),
)
