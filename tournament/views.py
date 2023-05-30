from django.contrib import messages

from django.shortcuts import render, redirect
from django.views.generic import View, ListView, FormView
from . forms import TournamentForm
from . models import Tournament

# Create your views here.
class TournamentView(ListView, FormView):
    model = Tournament
    context_object_name = "tournament"
    template_name = "scores/team_players.html"

    form_class = TournamentForm
    # success_url = reverse_lazy("auth:team_players", id)

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        return super().get_context_data(**kwargs)

    def post(self, request, id, *args, **kwargs):
        form = self.form_class(request.POST)
      
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(self.request, "Player Added to Team")

            return redirect("auth:team_players", id)
        else:
            messages.error(self.request, f"An error occured")
            return self.form_invalid(form)

class TournamentFormView(View):
    form_class = TournamentForm
    template_name = 'tournament/tournament_modal.html'

class RectorCupView(ListView, FormView):
    model = Tournament
    context_object_name = "rector"
    template_name = "tournament/rector_cup.html"

    form_class = TournamentForm
    # success_url = reverse_lazy("auth:team_players", id)

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.filter(name='rector_cup')
        return super().get_context_data(**kwargs)

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


