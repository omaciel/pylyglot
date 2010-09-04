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
from pylyglot.core.models import Sentence, Translation, Word

def index(request):

    result = {}
    translations = []
    language_id = 1

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            language_id = form.cleaned_data['languages']

            words = Word.objects.filter(term__contains=query).order_by('term')
            for word in words:
                trans = []
                translations = Translation.objects.filter(words__term=word.term, language__id=language_id).order_by('msgid__length')
                if translations:
                    for translation in translations:
                        trans.append(translation)
                    result[word.term] = trans
                else:
                    words.pop(word)
    else:
        form = SearchForm()

    variables = RequestContext(request, {
        'object_list': result,
        'language_id': language_id,
        'form': form,
        })

    return render_to_response('translations/translation_list.html', variables)
