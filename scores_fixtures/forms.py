from django import forms

from . models import Fixture, Tournament, Team

class FixturesForm(forms.ModelForm):
    # tournament = forms.ModelChoiceField(queryset=Tournament.objects.all(), empty_label="Select Tournament", required=True, widget=forms.Select(
    #     attrs={
    #         'class':'form-control select form-select',
    #     }
    # ))
  
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