from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotModified
from lol_tourney.models import Summoner
from lol_tourney.forms import SignUpForm

def home(request):
    #registered = Summoner.objects.all()
    if (request.POST):
        pass
    else:
        pass
    form = SignUpForm()
    return render_to_response('index.html', {'form': form},
                               context_instance=RequestContext(request))

def matches(request):
    return render_to_response('index.html', context_instance=RequestContext(request))
'''
def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
'''
