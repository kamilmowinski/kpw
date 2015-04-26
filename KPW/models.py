from django.contrib.auth.models import User
from django.db import models


class Statistic(models.Model):
    url = models.CharField(max_length=250)
    user = models.ForeignKey(User)
    searched = models.CharField(max_length=250)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.url