from django.db import models
from django.contrib.auth.models import User



class Photo(models.Model):
    user = models.ForeignKey(User, related_name='photos')
    create_time = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.CharField(max_length=256)
    image_name = models.CharField(max_length=128)
    type = models.CharField(max_length=64)
    description = models.CharField(max_length=256)

    def __unicode__(self):
        return self.description