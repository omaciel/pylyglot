from django.db import models

class Package(models.Model):

    name = models.CharField(max_length=255)
    revisiondate = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name
