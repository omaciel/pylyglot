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
from pylyglot.core.forms import SearchForm
from pylyglot.core.models import Translation

def index(request):

    translations = []
    language_id = 1
    query = ''

    if "query" in request.GET:
        form = SearchForm(request.POST)
        is_searching = True
        if form.is_valid():
            query = form.cleaned_data['query']
            language_id = form.cleaned_data['languages']

            translations = Translation.objects.filter(
                    msgid__icontains=query,
                    language__id=language_id,
                ).order_by('length', 'msgid', 'package__name')
    else:
        form = SearchForm()
        is_searching = False

    variables = RequestContext(request, {
        'object_list': translations,
        'query': query,
        'language_id': language_id,
        'form': form,
        'is_searching': is_searching,
        })

    return render_to_response('translations/translation_list.html', variables)
