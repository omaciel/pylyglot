# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.shortcuts import render_to_response
from django.template import RequestContext
from bidu.core.forms import SearchForm
from bidu.core.models import Word
from bidu.translations.models import Translation

def index(request):

    translations = []
    language_id = 1

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            language_id = form.cleaned_data['languages']

            translations = Word.objects.filter(
                term__contains=query
                ).filter(sentence__translations__language__id=language_id
                        ).distinct()
    else:
        form = SearchForm()

    variables = RequestContext(request, {
        'object_list': translations,
        'language_id': language_id,
        'form': form,
        })

    return render_to_response('translations/translation_list.html', variables)
