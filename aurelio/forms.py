# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
            label = u'Search for:',
        widget = forms.TextInput(attrs={'size': 32})
    )

