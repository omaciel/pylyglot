# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django.db import models

class Word(models.Model):

    term = models.CharField(max_length=255)

    def __unicode__(self):
        return self.term

class Package(models.Model):

    name = models.CharField(max_length=255)
    revisiondate = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Sentence(models.Model):

    msgid = models.TextField()
    msgstr = models.TextField()
    length = models.IntegerField(blank=True, null=True)
    flags = models.CharField(max_length=255, blank=True, null=True)
    translated = models.BooleanField()

    packages = models.ManyToManyField(Package)
    words = models.ManyToManyField(Word)

    def __unicode_(self):
        return self.msgid.encode("utf-8")

    def __repr__(self):
        return u'<Sentence: %s>' % self.msgid.encode("utf-8")

    def save(self, *args, **kwargs):
        words = self.msgid.split(" ")
        self.length = len(words)

        super(Sentence, self).save(*args, **kwargs)
