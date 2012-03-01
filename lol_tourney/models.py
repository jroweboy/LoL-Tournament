from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Summoner(models.Model):
    # might implement this soon
    # icon     = models.IntegerField(default=0)
    user = models.OneToOneField(User) 
    summoner = models.CharField(max_length=30)
    skype    = models.CharField(max_length=30, blank=True)
    email    = models.CharField(max_length=40, blank=True)
    wins     = models.IntegerField(default=0)
    level    = models.IntegerField()
    is30     = models.BooleanField()
    def __unicode__(self):
        return 'Summoner: %s' %(self.summoner)

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = Summoner.objects.get_or_create(user=instance) 

class Match(models.Model):
    match    = models.ManyToManyField('Summoner', related_name='match')
    blue     = models.ManyToManyField('Summoner', related_name='blue')
    purple   = models.ManyToManyField('Summoner', related_name='purple')
    winner   = models.CharField(max_length=10,  blank=True)
    finished = models.BooleanField()
    def __unicode__(self):
        return 'Match winner: %s' %self.winner
    
# use the Summoner model as a extension of the User model
post_save.connect(create_user_profile, sender=User) 