# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django.contrib import admin
from aurelio.models import Sentence, Package, Word, Translation, Language

class TranslationAdmin(admin.ModelAdmin):
    pass

class LanguageAdmin(admin.ModelAdmin):
    pass

class SentenceAdmin(admin.ModelAdmin):
    pass

class PackageAdmin(admin.ModelAdmin):
    pass

class WordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Translation, TranslationAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Word, WordAdmin)
