# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from aurelio.forms import PackageSearchForm, SearchForm
from aurelio.models import *

def front_page(request):
    variables = RequestContext(request, {
        })
    return render_to_response('base.html', variables)

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

def packages_page(request):

    packages = []

    if request.method == 'POST':
        form = PackageSearchForm(request.POST)

        if form.is_valid():
            term = form.cleaned_data['query']
            packages = Package.objects.filter(name__icontains=term)

    else:
        form = PackageSearchForm()
        packages = Package.objects.all()

    variables = RequestContext(request, {
        'form': form,
        'packages': packages,
        })

    return render_to_response('packages.html', variables)
