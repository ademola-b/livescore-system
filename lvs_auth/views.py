from typing import Any, Dict
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (View, ListView, FormView,
                                  TemplateView, DeleteView, UpdateView)
from django.contrib.messages.views import SuccessMessageMixin

from .forms import LoginForm, TeamForm, TeamPlayerForm, Department, Tournament
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
                return redirect('auth:dashboard')
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
            # team_check = Team.objects.filter(deptName = instance.deptName).exists()
            # if team_check:
            #     team = Team.objects.get(deptName = instance.deptName)
            #     team.coach = form.cleaned_data['coach']
            #     team.tournaments = form.cleaned_data['tournaments']
            #     team.save()
            #     messages.success(self.request, "Team Details Succesfully Updated")
            # else:
            instance.save()
            messages.success(self.request, "Team Succesfully Added")
            return redirect("auth:team")

        else:
            messages.error(self.request, f"An error occured: {form.errors}")
            return self.form_invalid(form)
   
# class TeamFormView(View):
#     form_class = TeamForm
#     template_name = 'utils/team_modal.html'

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

        # queryset = kwargs.pop('object_list', None)
        # if queryset is None:
        #     self.object_list = self.model.objects.filter(team_id = self.kwargs['pk'])
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

# class TeamPlayersFormView(View):
#     form_class = TeamPlayerForm
#     template_name = 'utils/team_player_modal.html'

class DeletePlayer(SuccessMessageMixin, DeleteView):
    model = Player
    success_message = 'Player Deleted Successfully'
    # success_url = reverse_lazy('auth:team_players')
    
    def get_success_url(self):
        return reverse_lazy('auth:team_players', kwargs={'pk': self.request.POST['team_pk']} )

def updatePlayer(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == "POST":
        form = TeamPlayerForm(request.POST, instance=player)
        if form.is_valid():
            player.save()
            form.save()
            return redirect(reverse('auth:team_players'))
    
    else:
        form = TeamPlayerForm(instance=player)
    
    return render(request, "lvs_auth/team_players.html")


class UpdatePlayer(UpdateView):
    model = Player
    # template_name = "utils/update_player.html"
    template_name = "lvs_auth/update_player.html"
    form_class = TeamPlayerForm

    def get(self, request, pk, *args, **kwargs):
        player_detail = Player.objects.get(id= pk)
        form = self.form_class(instance = player_detail)
        return render(request, self.template_name, {"form":form})

    # def get_context_data(self, **kwargs: Any):
    #     context = super().get_context_data(**kwargs)
    #     print("hello")
    #     context['form'] = self.form_class(instance = player)
    #     context['form'].fields['name'].initial = "player_detail.name"
    #     context['act'] = 'Update'
    #     return context

    def get_success_url(self):
        return reverse_lazy('auth:team_players', kwargs={'pk': self.request.POST['team_pk']} )



    




