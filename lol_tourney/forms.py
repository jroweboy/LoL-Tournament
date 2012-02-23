from django.forms import ModelForm
from lol_tourney.models import Summoner

class SignUpForm(ModelForm):
    class Meta:
        model = Summoner
