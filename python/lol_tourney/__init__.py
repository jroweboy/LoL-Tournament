from models import *
from bs4 import BeautifulSoup
import urllib2
import urllib
import re

def add2Queue(summoner_id):
    summoner = Summoner.objects.get(id=summoner_id)
    summoner.in_queue = True
    summoner.save()
    
def scrapeInfo(name):
    #scrape the site to get their info 
    response = urllib2.urlopen('http://leagueofstats.com/search',
                       data=urllib.urlencode({'name': name, 'region': 'na'}))
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
        response = urllib2.urlopen(address)
        data = response.read()
        soup2 = BeautifulSoup(data)
        summoner['wins'] = int(soup2.find(text='Unranked').parent.nextSibling.contents[0])
        icontemp = soup2.find('img', {'class': 'profileIcon'}).attrs['src']
        summoner['icon'] = int(re.findall(r'\d+', icontemp)[0])
        return summoner
    else:
        #error -- couldn't find the user blah blah
        class SummonerNotFound(Exception):
            def __init__(self, value):
                self.parameter = value
            def __str__(self):
                return repr(self.parameter)
        raise SummonerNotFound("Could not scrape %s's information" % name)
