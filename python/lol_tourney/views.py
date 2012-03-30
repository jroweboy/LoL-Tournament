from bs4 import BeautifulSoup
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseNotModified
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from lol_tourney.forms import SignUpForm
from lol_tourney.models import Summoner
import urllib2
import urllib
import pystache
#import cStringIO
import settings

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

def queue(request):
    data = {
        'match':1,
        'blue':[
            {
                'league':'DotAliscious',
                'skype':'morrison.levi',
                'icon':'./assets/img/profileIcon9.jpg',
                'totalWins':353,
                'currentUser':True
            },
            {
                'league':'Kraator',
                'skype':'erkieliszweski',
                'icon':'./assets/img/profileIcon24.jpg',
                'totalWins': 440
            },
            {
                'league':'Nammon',
                'skype':'sorgeskype',
                'icon':'./assets/img/profileIcon23.jpg',
                'totalWins': 667
            },
            {
                'league':'VictorousSecret',
                'skype':'spencer_horrocks',
                'icon':'./assets/img/profileIcon14.jpg',
                'totalWins': 843,
                'captain':True
            },
            {
                'league':'Canas',
                'skype':'david.tijerino',
                'icon':'./assets/img/profileIcon13.jpg',
                'totalWins': 544
            }
        ],
        'purple':[
            {
                'league':'Sprognak',
                'skype':'sprognak',
                'icon':'./assets/img/profileIcon5.jpg',
                'totalWins': 502
            },
            {
                'league':'Ghostilocks',
                'skype':'ghostilocks',
                'icon':'./assets/img/profileIcon16.jpg',
                'totalWins': 808,
                'captain':True
            },
            {
                'league':'b0b d0e',
                'skype':'jroweboy',
                'icon':'./assets/img/profileIcon21.jpg',
                'totalWins': 224
            },
            {
                'league':'Metroshica',
                'skype':'landon.orr',
                'icon':'./assets/img/profileIcon11.jpg',
                'totalWins': 339
            },
            {
                'league':'RubenatorX',
                'skype':'rubenatorxy',
                'icon':'./assets/img/profileIcon24.jpg',
                'totalWins': 478
                }
            ],
        'skypeGroup': [
                'morrison.levi',
                'erkieliszweski',
                'sorgeskype',
                'spencer_horrocks',
                'david.tijerino'
            ],
        'isAdmin': False #fix dat later :)
    }
    import pdb; pdb.set_trace()
    #okay, so using his hard coded data, I'm going to use use pystache to produce the code to output it
    
    return render_to_response('queue.html', {'data': renderMatches(data, 'current_matches')},
                               context_instance=RequestContext(request))

def ajaxUpdateMatches(request):
    # TODO make it check for an ajax call
    pass

def renderMatches(data, filename):
    import pdb; pdb.set_trace()
    with open(settings.STATICFILES_DIRS[1] + "/%s.txt" %filename) as f:
        read = f.read()
    return pystache.render(read, data)

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
