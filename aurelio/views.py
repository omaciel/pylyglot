# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from aurelio.forms import *
from aurelio.models import *

def glossary_page(request):
  form = SearchForm()
  words = []
  show_results = False
  if 'query' in request.GET:
     show_results = True
     query = request.GET['query'].strip()
     if query:
       form = SearchForm({'query' : query})
       words = Word.objects.filter(
         term__icontains=query
       )[:10]
  variables = RequestContext(request, {
     'form': form,
     'words': words,
     'show_results': show_results,
  })
  if request.GET.has_key('ajax'):
    return render_to_response('word_list.html', variables)
  else:
    return render_to_response('glossary.html', variables)

