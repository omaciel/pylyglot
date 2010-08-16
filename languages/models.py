from django.db import models

class Language(models.Model):

    long_name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s (%s)" % (self.long_name, self.short_name)
