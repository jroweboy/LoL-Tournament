from django.forms import ModelForm
from lol_tourney.models import Summoner

class SignUpForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['summoner'].label = "Summoner Name"
        self.fields['skype'].label = 'Skype Id'
        self.fields['email'].label = "Email"
    class Meta:
        model = Summoner
        fields = ['summoner', 'skype', 'email', ]
