from django import forms

from . models import Fixture

class FixturesForm(forms.ModelForm):

    class Meta:
        model = Fixture
        fields = "__all__"