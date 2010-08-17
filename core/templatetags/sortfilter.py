# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

# Snippet from http://djangosnippets.org/snippets/741/

from django.template import Library

register = Library()

def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

register.filter('order_by', order_by)
