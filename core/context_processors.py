# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.conf import settings

def templates_url(request):

    return {'template_url': settings.TEMPLATE_DIRS}
