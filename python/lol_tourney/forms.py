from django import forms
from django.forms import ModelForm, widgets
from lol_tourney.models import Summoner

class SignUpForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Summoner Name"
        self.fields['password'] = forms.CharField(widget=widgets.PasswordInput())
        self.fields['password'].label = "Password"
        self.fields['skype'].label = 'Skype Id'
        self.fields['email'].label = "Email"
    class Meta:
        model = Summoner
        fields = ['username', 'password', 'skype', 'email', ]
        
class SignUpFormTwo(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpFormTwo, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(widget=widgets.HiddenInput())
        self.fields['password'] = forms.CharField(widget=widgets.HiddenInput())
        self.fields['skype'] = forms.CharField(widget=widgets.HiddenInput(), required=False)
        self.fields['email'] = forms.CharField(widget=widgets.HiddenInput(), required=False)
        self.fields['level'].label = 'Levels'
        self.fields['wins'].label = "Estimate Wins"
    class Meta:
        model = Summoner
        fields = ['username', 'password', 'skype', 'email', 'level', 'wins',]

class SummonerInfo(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SummonerInfo, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Summoner
        fields = ['skype', 'email', 'level', 'wins', ]