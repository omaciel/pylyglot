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

from django.db import models
from pylyglot.translations.models import Translation

class Package(models.Model):

    name = models.CharField(max_length=255)
    src_url = models.URLField(verify_exists=False, blank=True, null=True)

    def __unicode__(self):
        return self.name

class Language(models.Model):

    long_name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s (%s)" % (self.long_name, self.short_name) if self.long_name else self.short_name

class Sentence(models.Model):

    msgid = models.TextField(max_length=1000)
    translated = models.BooleanField()
    length = models.IntegerField(blank=True, null=True)
    flags = models.CharField(max_length=255, blank=True, null=True)


    def __unicode__(self):
        return self.msgid

class Translation(models.Model):

    msgstr = models.TextField(max_length=1000)
    obsolete = models.BooleanField(default=False)

    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    language = models.ForeignKey(Language, db_index=True)
    package = models.ForeignKey(Package, db_index=True)
    sentence = models.ForeignKey(Sentence, db_index=True)

    def __unicode__(self):
        return self.msgstr
