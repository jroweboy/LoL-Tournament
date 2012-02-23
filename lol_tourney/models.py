from django.db import models

class Summoner(models.Model):
    summoner = models.CharField(max_length=30)
    skype    = models.CharField(max_length=30, blank=True)
    email    = models.CharField(max_length=40, blank=True)
    wins     = models.IntegerField(default=0)
    level    = models.IntegerField()
    is30     = models.BooleanField()
    
class Match(models.Model):
    match    = models.ManyToManyField('Summoner', related_name='match')
    blue     = models.ManyToManyField('Summoner', related_name='blue')
    purple   = models.ManyToManyField('Summoner', related_name='purple')
    finished = models.BooleanField()