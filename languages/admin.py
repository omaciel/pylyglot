# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.contrib import admin
from pylyglot.languages.models import Language

class LanguageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Language, LanguageAdmin)
