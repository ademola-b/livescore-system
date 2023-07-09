from django import forms
from django.contrib.auth.forms import AuthenticationForm
from scores_fixtures.models import GoalScorers, Match, MatchStats, Card

from tournament.models import Team, Department, Player, Tournament

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'id': 'email','class':'form-control', 'placeholder':'Enter your username', 'autofocus': 'true'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'id':'password','class':'form-control', 'placeholder':'***********'}))

class TeamForm(forms.ModelForm):

    deptName = forms.ModelChoiceField(queryset=Department.objects.exclude(deptName__in=[x.deptName for x in Team.objects.all()]), empty_label="Select Department", required=False, widget=forms.Select(
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

    tournaments = forms.ModelMultipleChoiceField(queryset = Tournament.objects.all(), required = False, widget=forms.CheckboxSelectMultiple()) 

    class Meta:
        model = Team
        fields = ["deptName", "coach", "tournaments"]

class TeamUpdateForm(forms.ModelForm):
    
    coach = forms.CharField(required = True, widget=forms.TextInput(
        attrs={
            'id': 'basic-default-name',
            'placeholder': 'Enter coach name',
            'class':'form-control',
        }
    )) 

    tournaments = forms.ModelMultipleChoiceField(queryset = Tournament.objects.all(), required = False, widget=forms.CheckboxSelectMultiple()) 

    class Meta:
        model = Team
        fields = ["coach", "tournaments"]

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
    

class UpdateMatchForm(forms.ModelForm):

    match_status = [
    ("not_started", "not_started"),
    ("ON", "ON"),
    ("HT", "HT"),
    ("FT", "FT"),
    ("ET", "ET"),
    ("postponed", "postponed"),
    ]

    status = forms.ChoiceField(choices=match_status, widget=forms.Select(
        attrs={
            'class': 'form-control select form-select'
        }
    ))

    referee = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    
    class Meta:
        model = Match
        fields = ['referee','status']


# class UpdateScoreForm(forms.ModelForm):
    # home_team_score = forms.CharField(widget=forms.NumberInput(
    #     attrs={
    #         'class': 'form-control'
    #     }
    # ))

    # away_team_score = forms.CharField(widget=forms.NumberInput(
    #     attrs={
    #         'class': 'form-control'
    #     }
    # ))

    # class Meta:
    #     model = Match
    #     exclude = "__all__"
    #     # fields = ['home_team_score', 'away_team_score']

    # def __init__(self, *args, **kwargs):
    #     pk = kwargs.pop('pk', None)
    #     super(UpdateScoreForm, self).__init__(*args, **kwargs)
    #     print(f"match: {pk}")
    #     match = Match.objects.get(pk = 1)

        # self.fields['home_team_score'].initial = match.home_team_score
        # self.fields['away_team_score'].initial = match.away_team_score
        
    # def clean_home_team_score(self):
    #     if int(self.cleaned_data['home_team_score']) < 0:
    #         raise forms.ValidationError("Invalid Score")
    
    # def clean_away_team_score(self):
    #     if int(self.cleaned_data['away_team_score']) < 0:
    #         raise forms.ValidationError("Invalid Score")
    
    # def save(self, commit=True):
    #     instance = super(UpdateScoreForm, self).save(commit=False)

    #     if commit:
    #         home_team_score = self.cleaned_data['home_team_score']
    #         away_team_score = self.cleaned_data['away_team_score']

    #         if int(instance.home_team_score) < home_team_score:
    #             raise forms.ValidationError("Invalid Score")
            
    #         if int(instance.away_team_score) < away_team_score:
    #             return "Invalid Score"
            
    #         instance.save()
    #         print(f"instance: {instance}")
        
class UpdateMatchStatusForm(forms.ModelForm):
    match_status = [
    ("not_started", "not_started"),
    ("ON", "ON"),
    ("HF", "HF"),
    ("FT", "FT"),
    ("ET", "ET"),
    ("postponed", "postponed"),
    ]

    status = forms.ChoiceField(choices=match_status, required=False, widget=forms.Select(
        attrs={
            'class': 'form-control select form-select', 'name':'status'
        }
    ))

    class Meta:
        model = Match
        fields = ["status"]

class UpdateGoalScorerForm(forms.ModelForm):

    team = forms.ModelChoiceField(queryset=Team.objects.none(), required=False, empty_label="Select Team", widget=forms.Select(
        attrs = {
            'class': 'form-control select form-select'
        }
    ))

    scorer = forms.ModelChoiceField(queryset=Player.objects.none(), required=False, empty_label="Select player", widget=forms.Select(
        attrs = {
            'class': 'form-control select form-select'
        }
    ))

    assist = forms.ModelChoiceField(queryset=Player.objects.none(), required=False, empty_label="Select player", widget=forms.Select(
        attrs = {
            'class': 'form-control select form-select'
        }
    ))
  
    class Meta:
        model = GoalScorers
        fields = [
            'team',
            'scorer',
            'assist',
        ]
        
class UpdateCardBookingForm(forms.ModelForm):
    red_card = forms.ModelChoiceField(queryset=Player.objects.none(), required=False, empty_label="Select player", widget=forms.Select(
        attrs = {
            'class': 'form-control select form-select'
        }
    ))
    yellow_card = forms.ModelChoiceField(queryset=Player.objects.none(), required=False, empty_label="Select player", widget=forms.Select(
        attrs = {
            'class': 'form-control select form-select'
        }
    ))

    class Meta:
        model = Card
        fields = [
            'red_card',
            'yellow_card'
        ]
 
class UpdateMatchStatForm(forms.ModelForm):

    corner = forms.ModelChoiceField(queryset=Team.objects.none(), required=False, empty_label="Select Team", widget=forms.Select(
        attrs = {
            'class': 'form-control select form-select'
        }
    ))

    foul = forms.ModelChoiceField(queryset=Team.objects.none(), required=False, empty_label="Select Team", widget=forms.Select(
        attrs = {
            'class': 'form-control select form-select'
        }
    ))

    offside = forms.ModelChoiceField(queryset=Team.objects.none(), required=False, empty_label="Select Team", widget=forms.Select(
        attrs = {
            'class': 'form-control select form-select'
        }
    ))


    class Meta:
        model = MatchStats
        fields = [
            'corner',
            'foul',
            # 'home_ball_possession',
            # 'away_ball_possession',
            'offside'
        ]

    def __init__(self, request, *args, **kwargs):
        super(UpdateMatchStatForm, self).__init__(*args, **kwargs)

        match = Match.objects.get(pk = kwargs['instance'].match_id)
        homeTeam = Team.objects.filter(team_id=match.fixture.home_team.team_id)
        awayTeam = Team.objects.filter(team_id=match.fixture.away_team.team_id)

        self.fields['corner'].queryset = homeTeam | awayTeam
        self.fields['foul'].queryset = homeTeam | awayTeam
        self.fields['offside'].queryset = homeTeam | awayTeam
