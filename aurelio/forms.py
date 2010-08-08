# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django import forms
from aurelio.models import Language

class SearchForm(forms.Form):
    languages = forms.ModelChoiceField(
            label = u'Language:',
            queryset = Language.objects.all(),
    )
    query = forms.CharField(
            label = u'Search for:',
        widget = forms.TextInput(attrs={'size': 32})
    )

