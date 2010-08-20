# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.contrib import admin
from pylyglot.translations.models import Translation

class TranslationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Translation, TranslationAdmin)
