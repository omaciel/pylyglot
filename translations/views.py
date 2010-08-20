# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.shortcuts import render_to_response
from django.template import RequestContext
from core.forms import SearchForm
from bidu.translations.models import Translation

def index(request):

    translations = []

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            language = form.cleaned_data['languages']

            translations = Translation.objects.filter(
                language__id=language
                ).filter(sentence__words__term__contains=query
                ).order_by('sentence__length')
    else:
        form = SearchForm()

    variables = RequestContext(request, {
        'object_list': translations,
        'form': form,
        })

    return render_to_response('translations/translation_list.html', variables)
