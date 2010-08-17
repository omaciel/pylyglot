# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.shortcuts import render_to_response
from django.template import RequestContext
from aurelio.forms import PackageSearchForm, SearchForm
from aurelio.models import *
from bidu.languages.models import Language
from bidu.packages.models import Package

def index(request):

    packages = []
    translations = []
    language = 1

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            language = form.cleaned_data['languages']

            packages = Package.objects.filter(name__icontains=query)[:50]
            translations = Word.objects.filter(
                    term__contains=query,
                    sentence__translations__language__id=language
                ).distinct()
            #form = SearchForm({'query' : query})
    else:
        form = SearchForm()

    languages = Language.objects.count()
    latest_packages = Package.objects.all().order_by("-revisiondate")[:10]

    variables = RequestContext(request, {
        'packages': packages,
        'translations': translations,
        'languages': languages,
        'latest_packages': latest_packages,
        'languageid': language,
        'form': form,
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
