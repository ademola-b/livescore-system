import datetime
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (ListView, FormView, TemplateView,
                                   View, UpdateView, DeleteView)
from django.shortcuts import render, redirect


from . forms import FixturesForm
from . models import Fixture, Tournament, Team, Match
# Create your views here.

def HomeViewL(request):
    context = {}
    current_date = datetime.date.today()
    fixture_date = Fixture.objects.filter(match_date_time__date = current_date)
    context['today_match'] = Match.objects.filter(fixture__in=fixture_date)
    context["rector_fixture"] = Fixture.objects.filter(tournament__name = "rector_cup")
    context["dept_fixture"] = Fixture.objects.filter(tournament__name = "departmental")
    if request.htmx:
        return render(request, "utils/match_card.html", context)
    else:
        return render(request, "scores_fixtures/index.html", context=context)

class HomeView(ListView):
    model = Fixture
    context_object_name = "matches"
    template_name = "scores_fixtures/index.html"
    # current_date = timezone.now().date()
    current_date = datetime.date.today()
    # print(f"current date: {current_date}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fixture_date = Fixture.objects.filter(match_date_time__date = self.current_date)
   
        context['today_match'] = Match.objects.filter(fixture__in=fixture_date)
        # context['home_team'] = 
        context["rector_fixture"] = Fixture.objects.filter(tournament__name = "rector_cup")
        context["dept_fixture"] = Fixture.objects.filter(tournament__name = "departmental")
        return context
    

class FixturesView(LoginRequiredMixin, SuccessMessageMixin, TemplateView, ListView, FormView):
    login_url = "auth:login"
    model = Fixture
    context_object_name = "rector"
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

        # load form
        form = self.form_class()
        form.fields['tournament'].required = False
        template_name = self.kwargs['template_name']
        if template_name == "rector-cup":
            tournament = Tournament.objects.get(name="rector_cup")
            # print(f"tournament: {tournament}")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
            # print("fixed")
        elif template_name == "departmental":
            tournament = Tournament.objects.get(name="departmental")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)

        # add to context based on the template_name
        if self.kwargs['template_name'] == "rector-cup":
            context["rector_fixture"] = Fixture.objects.filter(tournament__name = "rector_cup")            
        elif self.kwargs['template_name'] == "departmental":
            context["dept_fixture"] = Fixture.objects.filter(tournament__name = "departmental")

        # add form and template_name to context
        context['form'] = form
        context['template_name'] = template_name
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)            
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        form = self.form_class(request.POST)
        form.fields['tournament'].required = False
        template_name = self.kwargs['template_name']
        print(f"template: {template_name}")
        if template_name == "rector-cup":
            tournament = Tournament.objects.get(name="rector_cup")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.home_team = form.cleaned_data['home_team']
                instance.away_team = form.cleaned_data['away_team']
                instance.match_date_time = form.cleaned_data['match_date_time']

                if instance.home_team == instance.away_team:
                    messages.warning(request, "Both teams should be different")
                    return redirect("scores:fixtures", self.kwargs['template_name'])
                
                 # compare supplied date
                if instance.match_date_time.__lt__(timezone.now()):
                    messages.warning(request, "Older dates can't be supplied")
                    return redirect("scores:fixtures", self.kwargs['template_name'])
                    
                instance.tournament = tournament
                instance.save()
                Match.objects.create(
                 fixture = instance
                )
            
                return redirect("scores:fixtures", self.kwargs['template_name'])
            else:
                messages.error(request, f"An error occurred: {form.errors.as_text}")
        elif template_name == "departmental":
            tournament = Tournament.objects.get(name="departmental")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.home_team = form.cleaned_data['home_team']
                instance.away_team = form.cleaned_data['away_team']
                instance.match_date_time = form.cleaned_data['match_date_time']

                if instance.home_team == instance.away_team:
                    messages.warning(request, "Both teams should be different")
                    return redirect("scores:fixtures", self.kwargs['template_name'])
                
                # compare date supplied
                if instance.match_date_time.__lt__(timezone.now()):
                    messages.warning(request, "Older dates can't be supplied")
                    return redirect("scores:fixtures", self.kwargs['template_name'])
                    
                instance.tournament = tournament
                instance.save()
            
                return redirect("scores:fixtures", self.kwargs['template_name'])
            else:
                messages.error(request, f"An error occurred: {form.errors.as_text}")
        else:
            messages.error(request, f"An error occured: {form.errors.as_text}")
            return redirect("scores:fixtures", self.kwargs['template_name'])
        
        return self.render_to_response(context)

class UpdateFixtureView(LoginRequiredMixin, SuccessMessageMixin, UpdateView): 
    login_url = "auth:login"
    model = Fixture
    template_name = "scores_fixtures/update_rector_fixture.html"
    form_class = FixturesForm
    success_message = "Fixtures Updated Successfully"

    def get(self, request, pk, *args, **kwargs):
        fixture_detail = self.model.objects.get(id = pk)
        form = self.form_class(instance = fixture_detail)

        template_name = self.kwargs['template_name']
        if template_name == "rector-cup":
            tournament = Tournament.objects.get(name="rector_cup")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
            print("fixed")
        elif template_name == "departmental":
            tournament = Tournament.objects.get(name="departmental")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)

        # form.fields['home_team'].initial = Team.objects.get(deptName = fixture_detail.home_team.deptName)
        # form.fields['home_team'].queryset = Team.objects.filter(deptName = fixture_detail.home_team.deptName)
        return render(request, self.template_name, {"form":form})
    
    def post(self, request, pk, *args, **kwargs):
        fixture_detail = self.model.objects.get(id = pk)
        form = self.form_class(request.POST, instance = fixture_detail)
        form.fields['tournament'].required = False
        template_name = self.kwargs['template_name']

        if template_name == "rector-cup":
            tournament = Tournament.objects.get(name="rector_cup")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.home_team = form.cleaned_data['home_team']
                instance.away_team = form.cleaned_data['away_team']
                instance.match_date_time = form.cleaned_data['match_date_time']

                if instance.home_team == instance.away_team:
                    messages.warning(request, "Both teams can't be the same")
                    return redirect("scores:update_fixture", self.kwargs['template_name'], self.kwargs['pk'])
                
                 # compare supplied date
                if instance.match_date_time.__lt__(timezone.now()):
                    messages.warning(request, "Older dates can't be supplied")
                    return redirect("scores:update_fixture", self.kwargs['template_name'], self.kwargs['pk'])
                    
                instance.tournament = tournament
                instance.save()
            
                return redirect("scores:fixtures", self.kwargs['template_name'])
            else:
                messages.error(request, f"An error occurred: {form.errors.as_text}")
        elif template_name == "departmental":
            tournament = Tournament.objects.get(name="departmental")
            form.fields['home_team'].queryset = Team.objects.filter(tournaments = tournament)
            form.fields['away_team'].queryset = Team.objects.filter(tournaments = tournament)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.home_team = form.cleaned_data['home_team']
                instance.away_team = form.cleaned_data['away_team']
                instance.match_date_time = form.cleaned_data['match_date_time']

                if instance.home_team == instance.away_team:
                    messages.warning(request, "Both teams should be different")
                    return redirect("scores:fixtures", self.kwargs['template_name'])
                
                # compare date supplied
                if instance.match_date_time.__lt__(timezone.now()):
                    messages.warning(request, "Older dates can't be supplied")
                    return redirect("scores:fixtures", self.kwargs['template_name'])
                    
                instance.tournament = tournament
                instance.save()
            
                return redirect("scores:fixtures", self.kwargs['template_name'])
            else:
                messages.error(request, f"An error occurred: {form.errors.as_text}")
        else:
            messages.error(request, f"An error occured: {form.errors.as_text}")
            return redirect("scores:fixtures", self.kwargs['template_name'])
        
        return render(request, self.template_name, {"form":form}) 

    def get_success_url(self):
        return reverse_lazy('scores:fixtures', kwargs={'template_name': self.request.POST['template_name']})

class DeleteFixtureView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = "auth:login"
    model = Fixture
    success_message = "Fixture Deleted Successfully"

    def get_success_url(self):
        return reverse_lazy('scores:fixtures', kwargs={'template_name': self.request.POST['template_name']})

class MatchesView(LoginRequiredMixin, View):
    login_url = "auth:login"
    model = Match



    