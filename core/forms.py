# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-
#
# This file is part of Pylyglot.
#
# Pylyglot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylyglot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pylyglot.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from pylyglot.core.models import Language

class SearchForm(forms.Form):

    available_languages = Language.objects.all().values_list('id', 'short_name').order_by('short_name')

    languages = forms.ChoiceField(choices = available_languages)
    query = forms.CharField()

class PackageSearchForm(forms.Form):

    query = forms.CharField()
