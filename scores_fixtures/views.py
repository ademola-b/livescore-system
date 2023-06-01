from typing import List
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, FormView, TemplateView, View
from django.shortcuts import render, redirect


from . forms import FixturesForm
from . models import Fixture, Tournament, Team
# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'scores_fixtures/index.html')

class FixturesView(SuccessMessageMixin, TemplateView, ListView, FormView):
    model = Fixture
    # context_object_name = "rector"
    template_name = "scores_fixtures/rector_fixtures.html"
    object_list = Fixture.objects.all()
    success_message = "Fixtures Added"

    form_class = FixturesForm
    # success_url = reverse_lazy("auth:team_players", id)

    def get_template_names(self):
        template_name = self.kwargs.get('template_name')
        if template_name == 'rector-cup':
            return ["scores_fixtures/rector_fixtures.html"]
        elif template_name == 'departmental':
            return ["scores_fixtures/departmental_fixtures.html"]
        else:
            return ["utils/404.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        rector_fixture = Tournament.objects.get(name = "rector_cup")
        print(f"templa_name: {self.kwargs['template_name']}")
        if self.kwargs['template_name'] == "rector-cup":
            context["rector_fixture"] = Fixture.objects.filter(tournament__name = "rector_cup")
            print(f"dept fixture: {context['rector_fixture']}")
            
        elif self.kwargs['template_name'] == "departmental":
            context["dept_fixture"] = Fixture.objects.filter(tournament__name = "departmental")
      
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print(f"context: {context}")
        form = self.form_class()
        form.fields['tournament'].required = False
        template_names = self.get_template_names()
        template_name = self.kwargs['template_name']

        if template_name == "rector-cup":
            tournament = Tournament.objects.get(name="rector_cup")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
        elif template_name == "departmental":
            tournament = Tournament.objects.get(name="departmental")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
            
        return self.render_to_response(context)
        # return render(request, template_names, {"form":form})

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(self, **kwargs)
        
        form = self.form_class(request.POST)
        form.fields['tournament'].required = False
        template_name = self.kwargs['template_name']
        print(f"template: {template_name}")
        if template_name == "rector-cup":
            tournament = Tournament.objects.get(name="rector_cup")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
            if form.is_valid():
                print("form valid")
                instance = form.save(commit=False)
                instance.home_team = form.cleaned_data['home_team']
                instance.away_team = form.cleaned_data['away_team']
                print(f"Both teams: {instance.home_team} - {instance.away_team}")
                if instance.home_team == instance.away_team:
                    messages.warning(request, "Both teams should be different")
                    return redirect("scores:fixtures", self.kwargs['template_name'])
                instance.tournament = tournament
                instance.save()
            
                return redirect("scores:fixtures", self.kwargs['template_name'])
            else:
                messages.error(request, f"An error occurred: {form.errors.as_text}")
        elif template_name == "department":
            tournament = Tournament.objects.get(name="rector_cup")
            if form.is_valid():
                instance = form.save(commit=False)
                instance.tournament = tournament
                instance.save()
            
                return redirect("scores:fixtures", self.kwargs['template_name'])
        else:
            messages.error(request, f"An error occured: {form.errors.as_text}")
            return redirect("scores:fixtures", self.kwargs['template_name'])
        
        return self.render_to_response(context)

        # return render(request, self.template_name)
            

class RectorFixture(View):
    model = Fixture



    