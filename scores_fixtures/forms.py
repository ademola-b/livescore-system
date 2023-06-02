from django import forms

from . models import Fixture, Tournament, Team

class FixturesForm(forms.ModelForm):

  
    home_team = forms.ModelChoiceField(queryset=Team.objects.none(), empty_label="Select Home Team", required=True, widget=forms.Select(
        attrs={
            'class':'form-control select form-select',
        }
    ))
    
    away_team = forms.ModelChoiceField(queryset=Team.objects.none(), empty_label="Select Away Team", required=True, widget=forms.Select(
        attrs={
            'class':'form-control select form-select',
        }
    ))

    class Meta:
        model = Fixture
        fields = "__all__"

        widgets = {
            "match_date_time": forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            )
        }
    
    # def __init__(self, *args, **kwargs):
    #     template_name = kwargs.pop('template_name', None)
    #     super(FixturesForm, self).__init__(*args, **kwargs)

    #     if template_name == "rector_cup":
    #         tournament = Tournament.objects.get(name="rector_cup")
    #         self.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
    #         self.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
    #     elif template_name == "departmental":
    #         tournament = Tournament.objects.get(name="departmental")
    #         self.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
    #         self.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
