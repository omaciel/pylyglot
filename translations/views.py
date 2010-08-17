# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.shortcuts import render_to_response
from django.template import RequestContext
from aurelio.forms import PackageSearchForm, SearchForm
from aurelio.models import *

def index(request):

    translations = []
    language = 1

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            language = form.cleaned_data['languages']

            translations = Word.objects.filter(
                    term__contains=query,
                    sentence__translations__language__id=language
                ).distinct()
            #form = SearchForm({'query' : query})
    else:
        form = SearchForm()

    variables = RequestContext(request, {
        'object_list': translations,
        'languageid': language,
        'form': form,
        })

    return render_to_response('translations/translation_list.html', variables)
