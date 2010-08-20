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
