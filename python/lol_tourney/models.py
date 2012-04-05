from django.db import models
from datetime import datetime
#from django.contrib.auth.models import User
#from django.db.models.signals import post_save

class Summoner(models.Model):
    # might implement this soon
    icon     = models.IntegerField(default=0)
#    user = models.OneToOneField(User) 
    summoner = models.CharField(max_length=32, unique=True)
    skype    = models.CharField(max_length=32, blank=True)
    email    = models.CharField(max_length=32, blank=True)
    in_queue = models.BooleanField(default=False)
    wins     = models.IntegerField(default=0)
    level    = models.IntegerField(default=1)
    lan_wins = models.IntegerField(default=0) 
    played_today = models.IntegerField(default=0)
    #played_on = models.DateTimeField(blank=True)
    def __unicode__(self):
        return 'Summoner: %s' %(self.summoner)
    class Meta:
        db_table = 'summoners'

#class Status(models.Model):
#    name = models.CharField(max_length=32)
#    class Meta:
#        db_table = 'statuses' 

#class Outcome(models.Model):
#    name = models.CharField(max_length=32)
#    class Meta:
#        db_table = 'outcomes'

class Team(models.Model):
    #outcome = models.ForeignKey(Outcome)
    outcome = models.CharField(max_length=32, default='incomplete')
    players = models.ManyToManyField(Summoner)

    class Meta:
        db_table = 'teams'

class Match(models.Model):
    blue = models.ForeignKey(Team, related_name='blue')
    purple = models.ForeignKey(Team, related_name='purple')
    #display means it should appear in the box
    status = models.CharField(max_length=32, default='display')
    played_on = models.DateTimeField(default=datetime.now)
#    status = models.ForeignKey(Status)
#    blue     = models.ManyToManyField('Summoner', related_name='blue')
#    purple   = models.ManyToManyField('Summoner', related_name='purple')
#    def __unicode__(self):
#        return 'Match winner: %s' %self.winner

    class Meta:
        db_table = 'matches'
    
# use the Summoner model as a extension of the User model
#post_save.connect(create_user_profile, sender=User) 
