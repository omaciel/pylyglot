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

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from core.forms import SearchForm
from core.models import Translation
from django.db.models import Count

from django.views.generic import ListView

from django.views.generic import ListView

class SearchableTranslationListView(ListView):
    model = Translation
    paginate_by = 20
    template_name = 'translations/translation_list.html'

    def get_queryset(self):
        queryset = super(SearchableTranslationListView, self).get_queryset()
        self.query = self.request.GET.get('query', '')
        self.short_name = self.request.GET.get('languages', '')

        if self.query and self.short_name:
            return queryset.filter(
                sentence__msgid__icontains=self.query,
                language__short_name=self.short_name,
                obsolete=False,
                ).values(
                    'sentence__msgid',
                    'msgstr',
                    'sentence__length',
                    'package__name',
                    ).order_by(
                        'sentence__length',
                        'sentence__msgid',
                        'msgstr'
                        ).distinct()
        else:
            return queryset.none()

    def get_context_data(self, **kwargs):
        kwargs.update({
            'query': self.query,
            'short_name': self.short_name,
            'form': SearchForm(self.request.GET or None),
            'is_searching': ('query' in self.request.GET and
                'languages' in self.request.GET),
            'pagination_extra': urlencode({
                'languages': self.short_name,
                'query': self.query,
            }),
        })
        return super(SearchableTranslationListView,
            self).get_context_data(**kwargs)
