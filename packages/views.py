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

from django.core import serializers
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.forms import PackageSearchForm
from core.models import *
from django.db.models import Avg

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

def translation_packages(request):
    if request.method == 'POST':
        short_name = request.POST['short_name']
        msgid = request.POST['msgid']
        msgstr = request.POST['msgstr']

        queryset = Package.objects.filter(
                translation__language__short_name=short_name,
                translation__msgid=msgid, translation__msgstr=msgstr
            ).annotate(average_packages=Avg('name'))

        response = serializers.serialize('json', queryset)

        return HttpResponse(response, mimetype='application/json')
    else:
        return HttpResponseNotFound()
