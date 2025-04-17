from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from accounts.models import Worker
from projects.forms import ProjectScopedTaskForm
from projects.forms import ProjectForm
from projects.models import Project
from tasks.models import Task
from teams.models import Team


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/project_list.html"


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["admin_projects"] = Project.objects.filter(teams__admins=user).distinct()
        print(context["admin_projects"])
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ["name", "teams"]
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:list")

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user not in project.admins.all():
            return HttpResponseForbidden("You are not allowed to edit this project.")
        return super().dispatch(request, *args, **kwargs)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:list")


class ProjectTaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = ProjectScopedTaskForm
    template_name = "tasks/task_form.html"

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"pk": self.project.pk})

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs["pk"])
        user_admin_teams = Team.objects.filter(admins=request.user)
        if not self.project.teams.filter(pk__in=user_admin_teams).exists():
            return HttpResponseForbidden("You are not allowed to create tasks for this project.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        teams_admin = Team.objects.filter(
            admins=self.request.user
        ).distinct()

        team_members = Worker.objects.filter(team__in=teams_admin).distinct()

        kwargs["team_members"] = team_members
        return kwargs

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

