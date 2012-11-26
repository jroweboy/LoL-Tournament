
#from django.conf import settings
from django.http import HttpResponse#, HttpResponseRedirect#, \
#    HttpResponseNotModified
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
#from django.template import RequestContext
from lol_tourney.forms import SignUpForm, SignUpFormTwo
from lol_tourney.models import *
from __init__ import add2Queue, scrapeInfo#, getUserInfo

import pystache
import settings
import random

'''
TODO List:
=> Make matchmaking actually work (grab people from the queue blah)
=> Make the match list work for matches being setup (the middle column)
=> TESTING!
'''

def home(request):
    #how to get all the summoners in the database. 
    #registered = Summoner.objects.all()
    #make sure that they at least put in a summoner name
    if request.POST:
        #import pdb; pdb.set_trace()
        if 'level' in request.POST:
            form = SignUpFormTwo(request.POST)
            # if they failed to type it in they are gettin the default data fields huehuehue
            
            if not form.is_valid():
                print form.errors
            summoner = form.save(False)
            summoner.set_password(summoner.password)
            summoner.save()
            s = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if not s:
                print "didn't login!!!! That's not good :p "
            login(request, s)
            return render(request, 'index.html', {'form': form, 'summoner': summoner})
            
        #else: No need to use the else since the above always returns
        form = SignUpForm(request.POST)
        if form.is_valid():
            info = scrapeInfo(form.cleaned_data['username'])
            # save the info to the database
            if not info:
                return render(request, 'index.html', {'form': SignUpFormTwo(request.POST), 'round_two': True, 'error': "Well, I couldn't find your info"})
            summoner = form.save(False)
            summoner.icon = info['icon']
            summoner.level = info['level']
            summoner.wins = info['wins']
            summoner.set_password(summoner.password)
            summoner.save()
            s = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if not s:
                print "didn't login!!!!"
            login(request, s)
            return render(request, 'index.html', {'form': form, 'summoner': summoner})
        elif 'username' in form.errors.keys() and form.errors['username'][0] == 'User with this Username already exists.':
            s = authenticate(username=form['username'].value(), password=form['password'].value())
            if not s:
                del form.errors['username']
                form.errors['password'] = "Error: Password was incorrect. If you've never made an account before or forgot your password, please contact the admin"
                return render(request, 'index.html', {'form': form, 'error': "Looks like the password didn't match"})
            login(request, s)
            summoner = Summoner.objects.get(username=form['username'].value())
            return render(request, 'index.html', {'form': form, 'summoner': summoner})
        else:
            return render(request, 'index.html', {'form': form, 'error': True})
    else:
        form = SignUpForm()
    #render the index page
    return render(request, 'index.html', {'form': form})

@login_required
def queue(request):
    #okay, so using his hard coded data, I'm going to use use pystache to produce the code to output it
    datadata = {'data': ajaxUpdateMatches(request), 'queue': ajaxUpdateQueue(request)}
    return render(request, 'queue.html', datadata)

@login_required
def join_queue(request):
    # TODO need to stop people from joining queue if they are in a match lol
    # which might not happen anymore with the new login system
    request.user.in_queue = True
    request.user.save()
    return ajaxUpdateQueue(request)

@user_passes_test(lambda u: u.is_superuser)
def kick_match(request):
    #me, admin = getUserInfo(request)
    # not logged in have them relogin :?
    #if not admin or not me:
    #    return HttpResponse('Not authenticated', status=403)
    person = request.POST['kickee']
    match_id = request.POST['match_id']
    if not match_id or not person:
        return HttpResponse('Not authenticated', status=403)
    #match = Match.objects.get(pk=match_id)
    kickee = Summoner.objects.get(summoner=person)
    # beautiful... found a limitation of the DB design right thar!
    try: 
        team = kickee.team_set.get(blue__pk=match_id)
    except: 
        try:
            team = kickee.team_set.get(purple__pk=match_id)
        except:
            return HttpResponse('Not authenticated', status=403)
    
    new_guy = Summoner.objects.filter(in_queue=True).order_by('?')[0]
    team.players.add(new_guy)
    team.players.remove(kickee)
    kickee.in_queue = True
    new_guy.in_queue = False
    kickee.save()
    new_guy.save()
    return ajaxUpdateQueue(request)

@user_passes_test(lambda u: u.is_superuser)
def finishMatch(request):
    match_id = request.POST['match_id']
    winner = request.POST['winner']
    match = Match.objects.get(pk=match_id)
    match.status = winner
    if winner == 'blue':
        match.blue.outcome = 'win'
        match.purple.outcome = 'lose'
    else:
        match.blue.outcome = 'lose'
        match.purple.outcome = 'win'
    match.save()
    return HttpResponse("Looks like work happened!")

@user_passes_test(lambda u: u.is_superuser)
def matchmake(request):
    ''' 
        How I added a match:
        Create two Team()
        save them first
        now add people to the team and the reverse
        teamA.players.add(summoner1)
        summoner1.team_set.add(teamA)
        then set match.blue = teamA and so forth
    '''
    #inqueue = random.shuffle(Summoner.objects.filter(in_queue=True))
    #being lazy using SQL Random
    inqueue = Summoner.objects.filter(in_queue=True).order_by('?')[:10]
    if len(inqueue) < 10:
        #TODO fix this to be a more approriate response
        return HttpResponse('Not authenticated', status=403)
    purple = inqueue[0:5]
    blue = inqueue[5:10]
    team_blue = Team()
    team_purple = Team()
    team_blue.save()
    team_purple.save()
    for s in purple:
        team_purple.players.add(s)
        s.team_set.add(team_purple)
        s.in_queue = False
        s.save()
    for s in blue:
        team_blue.players.add(s)
        s.team_set.add(team_blue)
        s.in_queue = False
        s.save()
        
    team_blue.save()
    team_purple.save()
    match = Match()
    match.blue = team_blue
    match.purple = team_purple
    
    match.save()
        
    return ajaxUpdateMatches(request)

@login_required
def ajaxUpdateQueue(request):
    #if not request.is_ajax():
    #    return HttpResponse(403)
    summoners = Summoner.objects.filter(in_queue=True)
    data = {}
    queue = []
    #me, admin = getUserInfo(request)
    for s in summoners:
        queue.append(
            {'league': s.summoner,
             'totalWins' : s.wins, } 
        )
    data['queue'] = queue
    data['isAdmin'] = request.user.is_superuser
    data['numInQueue'] = len(summoners)
    if request.is_ajax():
        return HttpResponse(renderStache('ajax_queue', data))
    return renderStache('ajax_queue', data)

@login_required
def ajaxUpdateMatches(request):
    #if not request.is_ajax():
    #    return HttpResponse(403)
    # me is the current user
    #import pdb; pdb.set_trace()
    #me, admin = getUserInfo(request)
    
    matches = Match.objects.filter(status='display')
    output = ''
    
    for m in matches:
        data = {}
        data['blue'] = []
        data['purple'] = []
        # convert the Summoner objects on each team into a list of dictionaries for the template
        for p in m.blue.players.all():
            s = {}
            if request.user == p:
                s['currentUser'] = True
            s['league'] = p.summoner
            s['skype'] = p.skype
            s['totalWins'] = p.wins
            s['icon'] = '%sassets/img/profileIcon%s.jpg' %(settings.STATIC_URL, p.icon)
            data['blue'].append(s)
        for p in m.purple.players.all():
            s = {}
            if request.user == p:
                s['currentUser'] = True
            s['league'] = p.summoner
            s['skype'] = p.skype
            s['totalWins'] = p.wins
            s['icon'] = '%sassets/img/profileIcon%s.jpg' %(settings.STATIC_URL, p.icon)
            data['purple'].append(s)
        
        data['isAdmin'] = request.user.is_superuser
        data['match_id'] = m.pk
        output += renderStache('ajax_match', data)
    
    if request.is_ajax():
        return HttpResponse(output)
    return output
    
def renderStache(filename, data):
    #stupid windows fix for the static dirs. I have to have a seperate folder for the symlink
    try :
        with open(settings.STATICFILES_DIRS[1] + "/%s.html" % filename) as f:
            read = f.read()
    except:
        with open(settings.STATICFILES_DIRS[3] + "/%s.html" % filename) as f:
            read = f.read()
    return pystache.render(read, data)


#def matches(request):
#    return render_to_response('index.html', context_instance=RequestContext(request))

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


'''
below is used solely for recreating the database again

from lol_tourney.models import *

blue = [{'league':'DotAliscious', 'skype':'morrison.levi', 'icon': 9, 'totalWins':353, 'currentUser':True}, {'league':'Kraator', 'skype':'erkieliszweski', 'icon': 24, 'totalWins': 440}, {'league':'Nammon', 'skype':'sorgeskype', 'icon':23, 'totalWins': 667}, {'league':'VictorousSecret', 'skype':'spencer_horrocks', 'icon':14, 'totalWins': 843, 'captain':True}, {'league':'Canas', 'skype':'david.tijerino', 'icon':13, 'totalWins': 544}]
purple = [{'league':'Sprognak', 'skype':'sprognak', 'icon':5, 'totalWins': 502}, {'league':'Ghostilocks', 'skype':'ghostilocks', 'icon':16, 'totalWins': 808, 'captain':True}, {'league':'b0b d0e', 'skype':'jroweboy', 'icon':21, 'totalWins': 224}, {'league':'Metroshica', 'skype':'landon.orr', 'icon':11, 'totalWins': 339}, {'league':'RubenatorX', 'skype':'rubenatorxy', 'icon':24, 'totalWins': 478}]

for b in blue:
 s = Summoner()
 s.username = b['league']
 s.skype = b['skype']
 s.icon = b['icon']
 s.wins = b['totalWins']
 s.level = 30
 s.in_queue = True
 s.set_password('a')
 s.save()

for b in purple:
 s = Summoner()
 s.username = b['league']
 s.skype = b['skype']
 s.icon = b['icon']
 s.wins = b['totalWins']
 s.level = 30
 s.in_queue = True
 s.set_password('a')
 s.save()


'skypeGroup': [                'morrison.levi', 'erkieliszweski',
                'sorgeskype',
                'spencer_horrocks',
                'david.tijerino'
            ],
        'isAdmin': True #fix dat later :)
    }


for b in blue:
 s = Summoner()
 s.summoner = b['league']
 s.skype = b['skype']
 s.icon = b['icon']
 s.wins = b['totalWins']
 s.level = 30
 s.save()

for b in purple:
 s = Summoner()
 s.summoner = b['league']
 s.skype = b['skype']
 s.icon = b['icon']
 s.wins = b['totalWins']
 s.level = 30
 s.save()



    for b in blue:
        s = Summoner()
        s.summoner = b['league']
        s.skype = b['skype']
        s.icon = b['icon']
        s.wins = b['totalWins']
        s.save()
    for b in data['purple']:
        s = Summoner()
        s.summoner = b['league']
        s.skype = b['skype']
        s.icon = b['icon']
        s.wins = b['totalWins']
        s.save()
    
    data = {
        'match':1,
        'blue':[
            {
                'league':'DotAliscious',
                'skype':'morrison.levi',
                'icon': 9,
                'totalWins':353,
                'currentUser':True
            },
            {
                'league':'Kraator',
                'skype':'erkieliszweski',
                'icon': 24,
                'totalWins': 440
            },
            {
                'league':'Nammon',
                'skype':'sorgeskype',
                'icon':23,
                'totalWins': 667
            },
            {
                'league':'VictorousSecret',
                'skype':'spencer_horrocks',
                'icon':14,
                'totalWins': 843,
                'captain':True
            },
            {
                'league':'Canas',
                'skype':'david.tijerino',
                'icon':13,
                'totalWins': 544
            }
        ],
        'purple':[
            {
                'league':'Sprognak',
                'skype':'sprognak',
                'icon':5,
                'totalWins': 502
            },
            {
                'league':'Ghostilocks',
                'skype':'ghostilocks',
                'icon':16,
                'totalWins': 808,
                'captain':True
            },
            {
                'league':'b0b d0e',
                'skype':'jroweboy',
                'icon':21,
                'totalWins': 224
            },
            {
                'league':'Metroshica',
                'skype':'landon.orr',
                'icon':11,
                'totalWins': 339
            },
            {
                'league':'RubenatorX',
                'skype':'rubenatorxy',
                'icon':24,
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
        'isAdmin': True #fix dat later :)
    }
'''