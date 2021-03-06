from models import *
from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import settings

def add2Queue(summoner_id):
    summoner = Summoner.objects.get(id=summoner_id)
    summoner.in_queue = True
    summoner.save()
    
def scrapeInfo(name):
    try:
        return scrapeInfo_los(name)
    except:
        return False

def scrapeInfo_los(name):
    #scrape the site to get their info 
    try :
        response = urllib2.urlopen('http://leagueofstats.com/search',
                       data=urllib.urlencode({'name': name, 'region': 'na'}))
    except:
        raise SummonerNotFound("Unable to contact the site")
    data = response.read()
    #BeautifulSoup is the html parser
    soup = BeautifulSoup(data)
    #the line below will out a breakpoint in the code 
    #import pdb; pdb.set_trace()
    if soup.find('div', {'class': 'search-result', }):
        summoner = {}
        # scrape out their level
        summoner['level'] = int(soup.find('div', {'class': 'search-result', },).p.next.next.next.split('\n')[1])
                
        # go to the match history page and scrape everything else
        address = 'http://leagueofstats.com' + soup.find('div', {'class': 'search-result', },).a['href']
        try :
            response = urllib2.urlopen(address)
        except :
            raise SummonerNotFound("")
        data = response.read()
        soup2 = BeautifulSoup(data)
        summoner['wins'] = int(soup2.find(text='Unranked').parent.nextSibling.contents[0])
        icontemp = soup2.find('img', {'class': 'profileIcon'}).attrs['src']
        summoner['icon'] = int(re.findall(r'\d+', icontemp)[0])
        return summoner
    else:
        raise SummonerNotFound("Could not scrape %s's information" % name)

#error -- couldn't find the user blah blah
class SummonerNotFound(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

"""
def getUserInfo(request):
    ''' 
        Takes in a session object and determines if the current user is an admin and
        which summoner they are. Returns a Summoner and a boolean isAdmin
    '''
    admin = False
    if 'summoner' in request.session:
        me = Summoner.objects.get(id=request.session['summoner'])
        if me.summoner in settings.APP_ADMINS:
            admin = True
    else:
        me = None
    return me, admin
"""