from django import forms

from . models import Tournament, Team
class TournamentForm(forms.ModelForm):

    # team = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label="Select Department", required=True, widget=forms.Select(
        attrs={
            'class':'form-control select form-select',
        }
    ))
    class Meta:
        model = Tournament
        fields = "__all__"

        widgets = {
            "name": forms.Select(attrs={

                'class':'form-control',
            }),
            # "team": forms.MultipleChoiceField(attrs={
                
            #     'class': 'form-control select form-select'
            # }),
            "session": forms.TextInput(attrs={
                'id': 'basic-default-name',
                'class':'form-control',
            })
        }