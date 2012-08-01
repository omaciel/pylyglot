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

    #created = models.DateField(auto_now_add=True)
    #last_modified = models.DateField(auto_now=True)

    language = models.ForeignKey(Language, db_index=True)
    package = models.ForeignKey(Package, db_index=True)
    sentence = models.ForeignKey(Sentence, db_index=True)

    def __unicode__(self):
        return self.msgstr

class Job(models.Model):
    """
    In [1]: languages = Language.objects.all()

    In [2]: packages = Package.objects.all()

    In [3]: for package in packages:
        for language in languages:
            (job, created) = Job.objects.get_or_create(language=language, package=package)
       ....:         job.save()
       ....:

    """

    last_updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    update_on = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)

    language = models.ForeignKey(Language, db_index=True)
    package = models.ForeignKey(Package, db_index=True)

    def save(self, *args, **kwargs):
        super(Job, self).save(*args, **kwargs)
        # Set update_on to end of queue
        end_queue = Job.objects.latest("update_on")
        if not end_queue or not end_queue.update_on:
            end_of_line = self.last_updated
        else:
            end_of_line = end_queue.update_on
        # Now, add 5 minutes to it!
        from datetime import timedelta
        five_minutes = timedelta(minutes=5)

        self.update_on = end_of_line + five_minutes
        super(Job, self).save(*args, **kwargs)
