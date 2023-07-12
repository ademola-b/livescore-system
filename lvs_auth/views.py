import datetime
from typing import Any, Dict
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

from scores_fixtures.models import Match, MatchStats, Fixture

from .forms import (LoginForm, TeamForm,TeamPlayerForm, TeamUpdateForm, 
                    Tournament, UpdateGoalScorerForm, UpdateCardBookingForm, 
                    UpdateMatchForm, UpdateMatchStatusForm, UpdateMatchStatForm, AdditionalInfoForm)
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
    form_class = TeamUpdateForm
    success_message = "Team detail updated"

    def get(self, request, pk, *args, **kwargs):
        team_detail = Team.objects.get(team_id= pk)
        form = self.form_class(instance = team_detail)
        team_tournament = Team.objects.filter(tournaments__id = 2)
        tourn = Tournament.objects.all()
        print(f"tournaments: {team_tournament}")
        # form.fields['deptName'].required = False
        return render(request, self.template_name, {"form":form, "team":team_detail})
    
    def post(self, request, pk):
        team_detail = Team.objects.get(team_id= pk)
        form = self.form_class(request.POST, instance=team_detail)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.deptName = team_detail.deptName
            instance.save()
            form.save()
            
            return self.form_valid(form)
        else:
            messages.warning(request, f"An error occurred: {form.errors.as_text}")
        return redirect("auth:team")

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
        # context["team_name"] = Match.objects.get(id = match_id)
        context["team"] = Match.objects.get(id = match_id)
        return context
    
    def match_time(self):
        match = Match.objects.get(fixture__match_date_time__date=datetime.date.today())
        global scheduler
        if match.status != 'not_started':
            match.time += 1
            print(f"time: {match.time}")
            match.save()
        elif match.status == 'FT':
            scheduler.remove_job('time_0001')

    
    # def form_valid(self, request, form):
    #     if form.is_valid():
    #         instance = form.save(commit=False)
    #         # print(f"time now: {now}")
    #         form.save()
    #         return super().form_valid(form)
    #     else:
    #         messages.warning(request, "An error occurred")
    #         return self.form_invalid(form)

# class UpdateMatchStat(SuccessMessageMixin, UpdateView):
#     model = MatchStats
#     template_name = "lvs_auth/update_match_score.html"
#     success_message = "Match Stats Successfully Updated"
    
#     def post()

class UpdateMatchScoreV(SuccessMessageMixin, UpdateView):
    model = Match
    template_name = "lvs_auth/update_match_score.html"
    form_class = UpdateGoalScorerForm
    second_form_class = UpdateMatchStatusForm
    third_form_class = UpdateCardBookingForm
    fourth_form_class = UpdateMatchStatForm
    fifth_form_class = AdditionalInfoForm

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        match_id = self.kwargs['pk']
        match = Match.objects.get(pk = match_id)
        match_stats = MatchStats.objects.update_or_create(match = match)
        print(f"match_status: {match_stats}")
        context['matchStatusForm'] = self.second_form_class(instance=match)
        context['matchStatsForm'] = self.fourth_form_class(self.request, instance=match_stats[0])
        context['additionalInfoForm'] = self.fifth_form_class()
        
        # instantiate forms
        goalScorerForm = self.form_class()
        cardBookingForm = self.third_form_class()
        # matchStatsForm = self.fourth_form_class(self.request, instance=match_stats[0])

        # query teams and players to be filled in select box
        homeTeam = Team.objects.filter(team_id=match.fixture.home_team.team_id)
        awayTeam = Team.objects.filter(team_id=match.fixture.away_team.team_id)

        homePlayers = Player.objects.filter(team_id=match.fixture.home_team)
        awayPlayers = Player.objects.filter(team_id=match.fixture.away_team)

        goalScorerForm.fields['team'].queryset = homeTeam | awayTeam
        goalScorerForm.fields['scorer'].queryset = homePlayers | awayPlayers
        goalScorerForm.fields['assist'].queryset = homePlayers | awayPlayers

        cardBookingForm.fields['red_card'].queryset = homePlayers | awayPlayers
        cardBookingForm.fields['yellow_card'].queryset = homePlayers | awayPlayers

        # matchStatsForm.fields['corner'].queryset = homeTeam | awayTeam

        context['goalScorerForm'] = goalScorerForm
        context['cardBookingForm'] = cardBookingForm
        context['match_time'] = match.time
        # context['matchStatsForm'] = matchStatsForm

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        match = Match.objects.get(pk = self.kwargs['pk'])
        match_stats = MatchStats.objects.update_or_create(match = match)
        
        goalScorerForm = self.form_class(request.POST)
        matchStatusForm = self.second_form_class(request.POST, instance=match)
        cardBookingForm = self.third_form_class(request.POST)
        matchStatsForm = self.fourth_form_class(request, request.POST, instance=match_stats[0])
        additionalInfoForm = self.fifth_form_class(request.POST)

        homeTeam = Team.objects.filter(team_id=match.fixture.home_team.team_id)
        awayTeam = Team.objects.filter(team_id=match.fixture.away_team.team_id)

        homePlayers = Player.objects.filter(team_id=match.fixture.home_team)
        awayPlayers = Player.objects.filter(team_id=match.fixture.away_team)

        goalScorerForm.fields['team'].queryset = homeTeam | awayTeam
        goalScorerForm.fields['scorer'].queryset = homePlayers | awayPlayers
        goalScorerForm.fields['assist'].queryset = homePlayers | awayPlayers

        cardBookingForm.fields['red_card'].queryset = homePlayers | awayPlayers
        cardBookingForm.fields['yellow_card'].queryset = homePlayers | awayPlayers

        print(f"request: {request.POST}")

        if 'score_btn' in request.POST:
            if goalScorerForm.is_valid():
                try:
                    goalScorerData = goalScorerForm.save(commit=False)
                    goalScorerData.team = goalScorerForm.cleaned_data['team']

                    print(f"scorer: {type(goalScorerData.scorer)}")

                    getTeam = Team.objects.get(team_id = goalScorerData.team.team_id)

                    print(f"scorer: {(goalScorerData.scorer.name)}")
                    print(f"scorer: {type(goalScorerData.scorer)}")

                    # get player
                    getPlayer = Player.objects.get(name = goalScorerData.scorer.name)
                    print(f"player_name: {getPlayer.name}")

                    #increment team's score
                    if getTeam == match.fixture.home_team:
                        match.home_team_score += 1
                        goalScorerData.home_score = match.home_team_score
                        print(f"match score: {match.home_team_score}")
                    elif getTeam == match.fixture.away_team:
                        match.away_team_score += 1

                        goalScorerData.away_score = match.away_team_score
                        print(f"match score: {match.away_team_score}")

                    #increment player's goals/assist number
                    if getPlayer == goalScorerData.scorer:
                        print("yes")
                        print(f"goal: {getPlayer.goals}")
                        # goalScorerData.
                        getPlayer.goals = getPlayer.goals + 1
                        print(f"goalN: {getPlayer.goals}")
                    
                    if getPlayer == goalScorerData.assist:
                        getPlayer.assists += 1

                    getPlayer.save()
                    goalScorerData.match = match
                    goalScorerData.time = match.time
                    goalScorerData.save()
                    match.save()

                    print(f"match: {match}")

                    messages.success(request, "Scores Updated Successfully")
                    return redirect("scores:index")
                except Team.DoesNotExist:
                    messages.warning(request, "No Update Made, you didn't select a team")
                    return redirect("scores:index")
            else:
                messages.warning(request, f"An error occurred: {goalScorerForm.errors.as_text()}")
        
        if 'status_btn' in request.POST:
            if  matchStatusForm.is_valid():
                matchStatusFormData = matchStatusForm.save(commit=False)
                matchStatusFormData.save() 

                messages.success(request, "Match Updated Successfully")
                return redirect('scores:index')
            else:
                messages.warning(request, f"An error occurred: {matchStatusForm.errors.as_text()}")

        if 'yellow' in request.POST:
            if cardBookingForm.is_valid():
                cardBookingFormData = cardBookingForm.save(commit=False)
                
                try:
                    getPlayer = Player.objects.get(name = cardBookingFormData.yellow_card.name)

                    if getPlayer == cardBookingFormData.yellow_card:
                        cardBookingFormData.match = match
                        cardBookingFormData.time = match.time
                        cardBookingFormData.yellow_card = getPlayer
                        cardBookingFormData.save()

                    messages.success(request, "Card successfully booked to player")
                    return redirect('scores:index')
                except Player.DoesNotExist:
                    messages.warning(request, "No player was selected")
            else:
                messages.warning(request, f"{cardBookingForm.errors.as_text()}")

        if 'red' in request.POST:
            if cardBookingForm.is_bound:
                print('httttt')
            if cardBookingForm.is_valid():
                cardBookingFormData = cardBookingForm.save(commit=False)
                # create or update model
                
                try:
                    getPlayer = Player.objects.get(name = cardBookingFormData.red_card.name)

                

                    if getPlayer == cardBookingFormData.red_card:
                        cardBookingFormData.match = match
                        cardBookingFormData.time = match.time
                        cardBookingFormData.red_card = getPlayer
                        cardBookingFormData.save()

                    print(f"player: {getPlayer}")
                    print(f"card player: {cardBookingFormData.red_card.name}")

                    messages.success(request, "Card successfully booked to player")
                    return redirect('scores:index')
                except Player.DoesNotExist:
                    messages.warning(request, "No player was selected")
        else:
            messages.warning(request, f"{cardBookingForm.errors.as_text()}")
        
        if 'match_stat_btn' in request.POST:
            # print(f"ww:{matchStatsForm}")
            if matchStatsForm.is_bound:
                print("bounded")
            if matchStatsForm.is_valid():
                matchStatsFormData = matchStatsForm.save(commit=False)
                print(f"corner: {matchStatsForm.cleaned_data['corner']}")
                #get team
                try:
                    if matchStatsForm.cleaned_data['corner'] is not None:
                        getTeam = Team.objects.get(team_id = matchStatsForm.cleaned_data['corner'].team_id)

                        print(f"team: {getTeam.team_id}")

                        if getTeam == match.fixture.home_team:
                            print("yes")
                            matchStatsFormData.home_corner +=1
                            matchStatsFormData.save()
                            messages.success(request, "Stats Saved Successfully")
                        elif getTeam == match.fixture.away_team:
                            matchStatsFormData.away_corner +=1
                        else:
                            messages.error(request, "Invalid Team Selected")
                    
                    if matchStatsForm.cleaned_data['foul'] is not None:
                        getTeam = Team.objects.get(team_id = matchStatsForm.cleaned_data['foul'].team_id)

                        print(f"team: {getTeam.team_id}")

                        if getTeam == match.fixture.home_team:
                            print("yes")
                            matchStatsFormData.home_fouls +=1
                            matchStatsFormData.save()
                            messages.success(request, "Stats Saved Successfully")
                        elif getTeam == match.fixture.away_team:
                            matchStatsFormData.away_fouls +=1
                        else:
                            messages.error(request, "Invalid Team Selected")
            
                    if matchStatsForm.cleaned_data['offside'] is not None:
                        getTeam = Team.objects.get(team_id = matchStatsForm.cleaned_data['offside'].team_id)

                        print(f"team: {getTeam.team_id}")

                        if getTeam == match.fixture.home_team:
                            print("yes")
                            matchStatsFormData.home_offside +=1
                            matchStatsFormData.save()
                            messages.success(request, "Stats Saved Successfully")
                        elif getTeam == match.fixture.away_team:
                            matchStatsFormData.away_offside +=1
                        else:
                            messages.error(request, "Invalid Team Selected")
                
                    return redirect('scores:index')
                except Team.DoesNotExist:
                    messages.warning(request, "Team Not Found")

            else:
                messages.warning(request, f"{matchStatsForm.errors.as_text()}")

        if 'additional_info_btn' in request.POST:
            print('hello')
            if additionalInfoForm.is_bound:
                print('yes')
            if additionalInfoForm.is_valid():
                additionalInfoFormData = additionalInfoForm.save(commit=False)

                additionalInfoFormData.match = match
                additionalInfoFormData.time = match.time
                additionalInfoFormData.save()
                messages.success(request, f"Additional Information added")
                return redirect('scores:index')
            else:
                messages.warning(request, f"{additionalInfoForm.errors.as_text()}")

        return self.render_to_response(self.get_context_data(matchStatusForm=matchStatusForm, goalScorerForm=goalScorerForm))