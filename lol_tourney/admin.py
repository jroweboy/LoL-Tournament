from django.contrib import admin
from lol_tourney.models import Summoner

class SummonerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Summoner, SummonerAdmin)