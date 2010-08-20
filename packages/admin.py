# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django.contrib import admin
from pylyglot.packages.models import Package

class PackageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Package, PackageAdmin)
