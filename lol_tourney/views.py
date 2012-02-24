from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotModified
from lol_tourney.models import Summoner
from lol_tourney.forms import SignUpForm
import urllib2, urllib
from bs4 import BeautifulSoup

def home(request):
    #registered = Summoner.objects.all()
    if request.POST and request.POST.get('summoner', ''):
        # temporary pass through for testing
        form = SignUpForm(request.POST)
        if form.is_valid():
            response = urllib2.urlopen('http://leagueofstats.com/search', 
                       data=urllib.urlencode({'name': form.cleaned_data['summoner'], 'region': 'na'}))
            data = response.read()
            soup = BeautifulSoup(data)
            #import pdb; pdb.set_trace()
            if soup.find('div', {'class': 'search-result',}):
                level = int(soup.find('div', {'class': 'search-result',},).p.next.next.next.split('\n')[1])
            else:
                #error blah blah
                pass
    else:
        form = SignUpForm()
    return render_to_response('index.html', {'form': form},
                               context_instance=RequestContext(request))

def matches(request):
    return render_to_response('index.html', context_instance=RequestContext(request))
'''
def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
'''
