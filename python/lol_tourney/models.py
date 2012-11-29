from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Summoner(User):
    # might use their icon picture at some point
    icon     = models.IntegerField(default=0)
    skype    = models.CharField(max_length=32, blank=True)
    in_queue = models.BooleanField(default=False)
    wins     = models.IntegerField(default=0)
    level    = models.IntegerField(default=1)
    lan_wins = models.IntegerField(default=0) 
    played_today = models.IntegerField(default=0)
    friends  = models.ManyToManyField("self")
    allow_add= models.BooleanField(default=1)
    def __unicode__(self):
        return self.username #'Summoner: %s' %(self.username)
    class Meta:
        db_table = 'summoners'

class Team(models.Model):
    outcome = models.CharField(max_length=32, default='incomplete')
    players = models.ManyToManyField(Summoner)
    class Meta:
        db_table = 'teams'

class Match(models.Model):
    blue = models.ForeignKey(Team, related_name='blue')
    purple = models.ForeignKey(Team, related_name='purple')
    #display means it should appear in the box
    #blue or purple denotes the winner
    status = models.CharField(max_length=32, default='display')
    played_on = models.DateTimeField(default=datetime.now)
    def __unicode__(self):
        return 'Match status: %s' %self.status
    def get_winner(self):
        if status == 'blue':
            return self.blue
        elif status == 'purple':
            return self.purple
        else:
            return False
    class Meta:
        db_table = 'matches'

#class ModelModel(models.Model):
#    ''' This model intentionally left blank '''
#    pass