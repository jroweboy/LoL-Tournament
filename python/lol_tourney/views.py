
from django.conf import settings
#from django.http import HttpResponse, HttpResponseRedirect, \
#    HttpResponseNotModified
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from lol_tourney.forms import SignUpForm
from lol_tourney.models import Summoner
from __init__ import *
import pystache

def home(request):
    #how to get all the summoners in the database. 
    #registered = Summoner.objects.all()
    #make sure that they at least put in a summoner name
    if request.POST and request.POST.get('summoner', ''):
        # temporary pass through for testing
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                info = scrapeInfo(form.cleaned_data['summoner'])
            except:
                # TODO add more appropriate error handling
                return render(request, 'index.html', {'form': form})
            # save the info to the database
            summoner = form.save(False)
            summoner.icon = info['icon']
            summoner.level = info['level']
            summoner.wins = info['wins']
            summoner.save()
            request.session['summoner'] = summoner.id
            return render(request, 'index.html', {'form': form, 'summoner': summoner})    
        elif 'summoner' in form.errors.keys():
            #Terrible error handling I know, but if they are in the database
            #just return their object from the database 
            summoner = Summoner.objects.get(summoner=form['summoner'].value())
            request.session['summoner'] = summoner.id
            return render(request, 'index.html', {'form': form, 'summoner': summoner})
    else:
        #first time through so no POST info yet
        form = SignUpForm()
    #render the index page
    return render(request, 'index.html', {'form': form})

def queue(request):
    import pdb; pdb.set_trace()
    
    data = {
        'match':1,
        'blue':[
            {
                'league':'DotAliscious',
                'skype':'morrison.levi',
                'icon':'%sassets/img/profileIcon9.jpg' %settings.STATIC_URL,
                'totalWins':353,
                'currentUser':True
            },
            {
                'league':'Kraator',
                'skype':'erkieliszweski',
                'icon':'%sassets/img/profileIcon24.jpg' %settings.STATIC_URL,
                'totalWins': 440
            },
            {
                'league':'Nammon',
                'skype':'sorgeskype',
                'icon':'%sassets/img/profileIcon23.jpg' %settings.STATIC_URL,
                'totalWins': 667
            },
            {
                'league':'VictorousSecret',
                'skype':'spencer_horrocks',
                'icon':'%sassets/img/profileIcon14.jpg' %settings.STATIC_URL,
                'totalWins': 843,
                'captain':True
            },
            {
                'league':'Canas',
                'skype':'david.tijerino',
                'icon':'%sassets/img/profileIcon13.jpg' %settings.STATIC_URL,
                'totalWins': 544
            }
        ],
        'purple':[
            {
                'league':'Sprognak',
                'skype':'sprognak',
                'icon':'%sassets/img/profileIcon5.jpg' %settings.STATIC_URL,
                'totalWins': 502
            },
            {
                'league':'Ghostilocks',
                'skype':'ghostilocks',
                'icon':'%sassets/img/profileIcon16.jpg' %settings.STATIC_URL,
                'totalWins': 808,
                'captain':True
            },
            {
                'league':'b0b d0e',
                'skype':'jroweboy',
                'icon':'%sassets/img/profileIcon21.jpg' %settings.STATIC_URL,
                'totalWins': 224
            },
            {
                'league':'Metroshica',
                'skype':'landon.orr',
                'icon':'%sassets/img/profileIcon11.jpg' %settings.STATIC_URL,
                'totalWins': 339
            },
            {
                'league':'RubenatorX',
                'skype':'rubenatorxy',
                'icon':'%sassets/img/profileIcon24.jpg' %settings.STATIC_URL,
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
    
    #okay, so using his hard coded data, I'm going to use use pystache to produce the code to output it
    datadata = {'data': renderStache('current_matches', data)}
    
    return render(request, 'queue.html', datadata)

def ajaxUpdateMatches(request):
    # TODO make it check for an ajax call
    pass

def renderStache(filename, data):
    with open(settings.STATICFILES_DIRS[1] + "/%s.html" %filename) as f:
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
