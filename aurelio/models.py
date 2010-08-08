# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django.db import models

class Language(models.Model):

    long_name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s (%s)" % (self.long_name, self.short_name)

class Word(models.Model):

    term = models.CharField(max_length=255)

    def __unicode__(self):
        return self.term

class Package(models.Model):

    name = models.CharField(max_length=255)
    revisiondate = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Translation(models.Model):

    msgstr = models.TextField()
    translated = models.BooleanField()

    language = models.ForeignKey(Language)

    def __unicode_(self):
        return self.msgstr.encode("utf-8")

class Sentence(models.Model):

    msgid = models.TextField()
    length = models.IntegerField(blank=True, null=True)
    flags = models.CharField(max_length=255, blank=True, null=True)

    packages = models.ManyToManyField(Package)
    words = models.ManyToManyField(Word)
    translations = models.ManyToManyField(Translation)

    def __unicode_(self):
        return self.msgid.encode("utf-8")

    def __repr__(self):
        return u'<Sentence: %s>' % self.msgid.encode("utf-8")
