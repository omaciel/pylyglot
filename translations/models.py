from django.db import models
from bidu.languages.models import Language

class Translation(models.Model):

    msgstr = models.TextField()
    translated = models.BooleanField()

    language = models.ForeignKey(Language)

    def __unicode_(self):
        return self.msgstr.encode("utf-8")
