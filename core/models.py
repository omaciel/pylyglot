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

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('package_detail', [str(self.id)])

class Language(models.Model):

    long_name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s (%s)" % (self.long_name, self.short_name)

class Word(models.Model):

    term = models.CharField(max_length=255, db_index=True)

    def __unicode__(self):
        return self.term

class Sentence(models.Model):

    msgid = models.TextField()
    length = models.IntegerField(blank=True, null=True)
    flags = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __unicode_(self):
        return self.msgid.encode("utf-8")

    def __repr__(self):
        return u'<Sentence: %s>' % self.msgid.encode("utf-8")

class Translation(models.Model):

    msgstr = models.TextField(max_length=1000)
    revisiondate = models.DateTimeField(blank=True, null=True)
    translated = models.BooleanField()
    standardized = models.NullBooleanField(default=False, blank=True, null=True)

    language = models.ForeignKey(Language, db_index=True)
    package = models.ForeignKey(Package, db_index=True)
    msgid = models.ForeignKey(Sentence, db_index=True)
    words = models.ManyToManyField(Word)

    def __unicode_(self):
        return self.msgstr.encode("utf-8")
