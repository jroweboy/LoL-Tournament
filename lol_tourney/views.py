from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotModified
from lol_tourney.models import Summoner
from lol_tourney.forms import SignUpForm
import urllib2, urllib
from bs4 import BeautifulSoup

def home(request):
    #how to get all the summoners in the database. 
    #registered = Summoner.objects.all()
    #make sure that they at least put in a summoner name
    if request.POST and request.POST.get('summoner', ''):
        # temporary pass through for testing
        form = SignUpForm(request.POST)
        if form.is_valid():
            #scrape the site to get their info 
            response = urllib2.urlopen('http://leagueofstats.com/search', 
                       data=urllib.urlencode({'name': form.cleaned_data['summoner'], 'region': 'na'}))
            data = response.read()
            #BeautifulSoup is the html parser
            soup = BeautifulSoup(data)
            #the line below will out a breakpoint in the code 
            #import pdb; pdb.set_trace()
            if soup.find('div', {'class': 'search-result',}):
                # scrape out their level
                level = int(soup.find('div', {'class': 'search-result',},).p.next.next.next.split('\n')[1])
                is30 = level == 30
                # go to the match history page
                address = 'http://leagueofstats.com' + soup.find('div', {'class': 'search-result',},).a['href']
                response = urllib2.urlopen(address)
                data = response.read()
                soup2 = BeautifulSoup(data)
                wins = int(soup2.find(text='Unranked').parent.nextSibling.contents[0])
                # save the info to the database
                summoner = form.save(False)
                summoner.is30 = is30
                summoner.level = level
                summoner.wins = wins
                summoner.save()
                return render_to_response('index.html', {'form': form, 'summoner': summoner},
                               context_instance=RequestContext(request))
                
            else:
                #error -- couldn't find the user blah blah
                pass
        #if everything is successful we should return a success page
    else:
        #first time through so no POST info yet
        form = SignUpForm()
    #render the index page
    return render_to_response('index.html', {'form': form},
                               context_instance=RequestContext(request))

def matches(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

# multi line comments are like that below
'''
def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
'''

'''
#matchmaking
team1 gets the highest lowest
then team2 get next 2 highest 2 lowest
then team1 get next highest lowest
split the last two to most even 
'''
