# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai
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

from django.contrib import admin
from core.lib import update_package

from pylyglot.core.models import Language, Package, Sentence, Translation

def create_task(modeladmin, request, queryset):
    for package in queryset.all():
        update_package(package)
create_task.short_description = "Update translations for this package."

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('long_name', 'short_name',)

class PackageAdmin(admin.ModelAdmin):
    actions = [create_task]

class TranslationAdmin(admin.ModelAdmin):
    list_filter = ['language', 'packages',]
    search_fields = ['msgstr', 'language',]

class SentenceAdmin(admin.ModelAdmin):
    search_fields = ['msgid',]

admin.site.register(Language, LanguageAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(Sentence, SentenceAdmin)
