# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.forms import PackageSearchForm
from core.models import *
from pylyglot.packages.models import Package

def index(request):

    packages = []

    if request.method == 'POST':
        form = PackageSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            packages = Package.objects.filter(
                    name__contains=query)
            #form = SearchForm({'query' : query})
    else:
        form = PackageSearchForm()

    variables = RequestContext(request, {
        'object_list': packages,
        'form': form,
        })

    return render_to_response('packages/package_list.html', variables)


def detail(request, object_id):
    try:
        p = Package.objects.get(pk=object_id)
        print p
    except Poll.DoesNotExist:
        raise Http404
    variables = RequestContext(request, {
        'object': p,
        })

    return render_to_response('packages/detail.html', variables)
