# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from pylyglot.languages.models import Language
from pylyglot.packages.models import Package
from pylyglot.translations.models import Translation

def total_packages(request):

    return {'total_packages': Package.objects.count()}

def total_languages(request):

    return {'total_languages': Language.objects.count()}

def total_translations(request):

    return {'total_translations': Translation.objects.count()}
