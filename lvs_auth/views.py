import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (View, ListView, FormView,
                                  TemplateView, DeleteView, UpdateView)
from django.contrib.messages.views import SuccessMessageMixin

from scores_fixtures.models import Match

from .forms import (LoginForm, TeamForm, 
                    TeamPlayerForm, Tournament, UpdateGoalScorerForm, UpdateMatchForm, UpdateScoreForm)
from tournament.models import Team, Player


# Create your views here.
class LoginView(View):
    template_name = 'lvs_auth/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('scores:index')
            else:
                messages.error(request, "User not found!")
        
        return render(request, self.template_name, {'form':form})
        
class DashboardView(TemplateView):
    def get(self, request):
        return render(request, 'lvs_auth/dashboard.html')

class TeamsView(ListView, FormView):
    model = Team
    context_object_name = "teams"
    template_name = 'lvs_auth/teams.html'
    object_list = Team.objects.all()

    form_class = TeamForm
    success_url = '/auth/teams/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournaments = Tournament.objects.all()
        if tournaments:
            context['tournaments'] = tournaments
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.success(self.request, "Team Succesfully Added")
            return redirect("auth:team")
        else:
            messages.error(self.request, f"An error occured: {form.errors}")
            return self.form_invalid(form)

class DeleteTeam(SuccessMessageMixin, DeleteView):
    model = Team
    success_message = 'Team Deleted Successfully'
    
    def get_success_url(self):
        return reverse_lazy('auth:team')

class UpdateTeam(SuccessMessageMixin, UpdateView):
    model = Team
    template_name = "lvs_auth/update_team.html"
    form_class = TeamForm
    success_message = "Team detail updated"

    def get(self, request, pk, *args, **kwargs):
        team_detail = Team.objects.get(team_id= pk)
        form = self.form_class(instance = team_detail)
        # team_tournament = Team.objects.filter(tournaments__name__in = [x for x in Tournament.objects.all()])
        team_tournament = Team.objects.filter(tournaments__id = 2)
        tourn = Tournament.objects.all()
        print(f"tournaments: {team_tournament}")
        form.fields['deptName'].required = False
        # form.fields['tournaments'].initial = Team.objects.filter(tournaments = tourn.id)
        return render(request, self.template_name, {"form":form, "team":team_detail})
    
    def post(self, request, pk):
        team_detail = Team.objects.get(team_id= pk)
        form = self.form_class(request.POST, instance=team_detail)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.deptName = team_detail.deptName
            instance.save()
            
            return self.form_valid(form)

    def get_success_url(self):
        return reverse_lazy('auth:team')

class TeamPlayers(ListView, FormView):
    model = Player
    context_object_name = "players"
    template_name = "lvs_auth/team_players.html"
    form_class = TeamPlayerForm
    # success_url = reverse_lazy("auth:team_players", id)

    def get_queryset(self):
        # qs = super().get_queryset()
        players = self.model.objects.filter(team_id = self.kwargs['pk'])
        return players
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_pk'] = self.kwargs['pk']
        return context

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        print(request.POST)
        team = Team.objects.get(team_id=pk)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.team_id = team
            instance.goals = 0
            instance.assists = 0
            instance.is_captain = False
            instance.save()
            messages.success(self.request, "Player Added to Team")

            return redirect("auth:team_players", pk)
        else:
            messages.error(self.request, f"An error occured")
            return self.form_invalid(form)

class DeletePlayer(SuccessMessageMixin, DeleteView):
    model = Player
    success_message = 'Player Deleted Successfully'
    # success_url = reverse_lazy('auth:team_players')
    
    def get_success_url(self):
        return reverse_lazy('auth:team_players', kwargs={'pk': self.request.POST['team_pk']} )
    
class UpdatePlayer(UpdateView):
    model = Player
    template_name = "lvs_auth/update_player.html"
    form_class = TeamPlayerForm

    def get(self, request, pk, *args, **kwargs):
        player_detail = Player.objects.get(id= pk)
        form = self.form_class(instance = player_detail)
        return render(request, self.template_name, {"form":form})

    def get_success_url(self):
        return reverse_lazy('auth:team_players', kwargs={'pk': self.request.POST['team_pk']} )
    

class UpdateMatch(SuccessMessageMixin, UpdateView):
    model = Match
    template_name = "lvs_auth/update_match.html"
    form_class = UpdateMatchForm
    success_message = "Match Updated"
    success_url = reverse_lazy('scores:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match_id = self.kwargs['pk']
        context["team_name"] = Match.objects.get(id = match_id)
        return context
    
    def form_valid(self, form: BaseForm):
        if form.is_valid():
            instance = form.save(commit=False)
            now = datetime.datetime.now().time()
            print(f"time now: {now}")
            # form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


def UpdateMatchScore(request, pk, *args, **kwargs):
    context = {}
    context['match'] = Match.objects.get(id=pk)
    if request.method == 'POST':
        matchScore = UpdateScoreForm(request.POST)
        goalScorer = UpdateGoalScorerForm(request.POST)
        
        if matchScore.is_valid() and goalScorer.is_valid():
            return render(request, 'lvs_auth/update_match_score.html')
        else:
            messages.error(f"An error occured:")
    else:
        context['matchScoreForm'] = UpdateScoreForm()
        context['goalScorerForm'] = UpdateGoalScorerForm()
        return render(request, 'lvs_auth/update_match_score.html', context)
 
    



    




