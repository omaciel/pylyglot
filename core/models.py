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

class Word(models.Model):

    term = models.CharField(max_length=255)

    def __unicode__(self):
        return self.term

class Sentence(models.Model):

    msgid = models.TextField()
    length = models.IntegerField(blank=True, null=True)
    flags = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    words = models.ManyToManyField(Word)
    translations = models.ManyToManyField(Translation)

    def __unicode_(self):
        return self.msgid.encode("utf-8")

    def __repr__(self):
        return u'<Sentence: %s>' % self.msgid.encode("utf-8")
