from django import forms
from django.contrib.auth.forms import AuthenticationForm

from tournament.models import Team, Department, Player, Tournament

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'id': 'email','class':'form-control', 'placeholder':'Enter your username', 'autofocus': 'true'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'id':'password','class':'form-control', 'placeholder':'***********'}))

class TeamForm(forms.ModelForm):

    deptName = forms.ModelChoiceField(queryset=Department.objects.exclude(deptName__in=[x.deptName for x in Team.objects.all()]), empty_label="Select Department", required=True, widget=forms.Select(
        attrs={
            'class':'form-control select form-select',
        }
    ))
    
    coach = forms.CharField(required = True, widget=forms.TextInput(
        attrs={
            'id': 'basic-default-name',
            'placeholder': 'Enter coach name',
            'class':'form-control',
        }
    )) 

    tournaments = forms.ModelMultipleChoiceField(queryset = Tournament.objects.all(), required = True, widget=forms.CheckboxSelectMultiple()) 

    class Meta:
        model = Team
        fields = ["deptName", "coach", "tournaments"]

class TeamPlayerForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
               }
    ))
    
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id': 'formFile',
            'class': 'form-control '
               }
    ))
    
    age = forms.CharField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control'
               }
    ))
    
    jersey_number = forms.CharField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control'
               }
    ))
    
    position = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
               }
    ))
    
    class Meta:
        model = Player
        fields = ["name", "image", "age", "jersey_number", "position"]
    

    