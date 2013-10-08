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
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import DetailView, ListView
from core.models import *
from django.db.models import Avg


class PackageListView(ListView):
    model = Package
    paginate_by = 20
    template_name = 'packages/package_list.html'


class PackageDetailView(DetailView):
    model = Package
    slug_field = 'name'
    template_name = 'packages/package_detail.html'

class PackageTranslationsListView(ListView):
    model = Translation
    paginate_by = 20
    template_name = 'packages/package_translations_list.html'

    def get_queryset(self):
        queryset = super(PackageTranslationsListView, self).get_queryset()
        return queryset.filter(package__name=self.kwargs['name'],
            language__short_name=self.kwargs['language'])

    def get_context_data(self, **kwargs):
        context = {
            'package': Package.objects.get(name=self.kwargs['name']),
            'language': Language.objects.get(short_name=self.kwargs['language']),
        }
        context.update(kwargs)

        return super(PackageTranslationsListView,
            self).get_context_data(**context)


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
