# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.shortcuts import render_to_response
from django.template import RequestContext
from aurelio.forms import PackageSearchForm, SearchForm
from aurelio.models import *

def index(request):
    packages = Package.objects.count()
    translations = Translation.objects.count()
    languages = Language.objects.count()
    latest_packages = Package.objects.all().order_by("-revisiondate")[:10]

    variables = RequestContext(request, {
        'packages': packages,
        'translations': translations,
        'languages': languages,
        'latest_packages': latest_packages,
        })
    return render_to_response('index.html', variables)

def translations_page(request):
    form = SearchForm()
    words = []
    language = 1
    query = ''
    show_results = False

    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        language = request.GET['languages'].strip()
        if query and language.isdigit():
            form = SearchForm({'query' : query})

            words = Word.objects.filter(
                    term__contains=query,
                    sentence__translations__language__id=language
                ).distinct()

    variables = RequestContext(request, {
        'form': form,
        'query': query,
        'words': words,
        'languageid': language,
        'show_results': show_results,
    })

    return render_to_response('glossary.html', variables)
