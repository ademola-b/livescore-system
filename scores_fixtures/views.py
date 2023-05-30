from typing import List
from django.contrib import messages
from django.views.generic import ListView, FormView, TemplateView, View
from django.shortcuts import render, redirect


from . forms import FixturesForm
from . models import Fixture, Tournament, Team
# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'scores_fixtures/index.html')
    
# class RectorFixturesFormView(View):
#     form_class = FixturesForm
#     template_name = 'scores_fixtures/tournament_modal.html'

class FixturesView(TemplateView, ListView, FormView):
    model = Fixture
    context_object_name = "rector"
    template_name = "scores_fixtures/rector_fixtures.html"
    object_list = Fixture.objects.all()

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


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        template_names = self.get_template_names()
        # team = Team.objects.get(id=3)
        # form.fields['home_team'].queryset = Tournament.objects.filter(team = team)  
        return render(request, template_names, {"form":form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        rector_team = Tournament.objects.get(name = "rector_cup")
        if rector_team:
            context['rector_team'] = self.model.objects.filter(tournament = rector_team)

        dept_team = Tournament.objects.get(name = "departmental")
        if dept_team:
            context['dept_team'] = self.model.objects.filter(tournament=dept_team)
        

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
      
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.success(self.request, "Team Added to Tournament")

            return redirect("tournament:rector_cup")
        else:
            messages.error(self.request, f"An error occured: {form.errors.as_text}")
            return self.form_invalid(form)



    