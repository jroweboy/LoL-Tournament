from django.db import models

class Summoner(models.Model):
    # might implement this soon
    # icon     = models.IntegerField(default=0)
    summoner = models.CharField(max_length=30)
    skype    = models.CharField(max_length=30, blank=True)
    email    = models.CharField(max_length=40, blank=True)
    wins     = models.IntegerField(default=0)
    level    = models.IntegerField()
    is30     = models.BooleanField()
    def __unicode__(self):
        return 'Summoner: %s' %(self.summoner)
    
class Match(models.Model):
    match    = models.ManyToManyField('Summoner', related_name='match')
    blue     = models.ManyToManyField('Summoner', related_name='blue')
    purple   = models.ManyToManyField('Summoner', related_name='purple')
    winner   = models.CharField(max_length=10,  blank=True)
    finished = models.BooleanField()
    def __unicode__(self):
        return 'Match winner: %s' %self.winner