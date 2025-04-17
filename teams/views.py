from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView

from teams.models import Team


class CreateTeamView(LoginRequiredMixin, CreateView):
    model = Team
    fields = ["name",]
    template_name = "teams/team_form.html"
    success_url = reverse_lazy("teams:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        team = self.object
        team.admins.add(self.request.user)
        team.workers.add(self.request.user)
        self.request.user.team = team
        self.request.user.save()
        return response

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "teams/team_list.html"


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "teams/team_detail.html"


class UpdateTeamView(LoginRequiredMixin, UpdateView):
    model = Team
    fields = ["name", "admins"]
    template_name = "teams/team_form.html"
    success_url = reverse_lazy("teams:list")

    def dispatch(self, request, *args, **kwargs):
        team = self.get_object()
        if request.user not in team.admins.all():
            return HttpResponseForbidden("You are not allowed to update this team.")
        return super().dispatch(request, *args, **kwargs)

class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = "teams/team_confirm_delete.html"
    success_url = reverse_lazy("teams:list")


class JoinTeamView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Team, pk=kwargs.get("pk"))
        team.workers.add(request.user)
        return redirect("teams:detail", pk=team.pk)


class LeaveTeamView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Team, pk=kwargs["pk"])
        team.workers.remove(request.user)
        return redirect("teams:detail", pk=team.pk)
