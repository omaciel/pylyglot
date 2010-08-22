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
from pylyglot.languages.models import Language
from pylyglot.packages.models import Package

class Translation(models.Model):

    msgstr = models.TextField()
    revisiondate = models.DateTimeField(blank=True, null=True)
    translated = models.BooleanField()

    language = models.ForeignKey(Language)
    package = models.ForeignKey(Package)

    def __unicode_(self):
        return self.msgstr.encode("utf-8")
