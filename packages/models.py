from django.db import models

class Package(models.Model):

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('package_detail', [str(self.id)])
