# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django import forms
from bidu.languages.models import Language

class SearchForm(forms.Form):

    available_languages = Language.objects.all().values_list('id', 'short_name')

    languages = forms.ChoiceField(choices = available_languages, initial="1")
    query = forms.CharField()

class PackageSearchForm(forms.Form):

    query = forms.CharField()
