# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django import forms
from aurelio.models import Language

class SearchForm(forms.Form):
    languages = Language.objects.all().values_list('id', 'short_name')
    available_languages = forms.ChoiceField(choices = languages, initial="1")
    query = forms.CharField(
            label = u'Search for:',
        widget = forms.TextInput(attrs={'size': 32})
    )

