# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.contrib import admin
from bidu.core.models import Sentence

class SentenceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sentence, SentenceAdmin)
