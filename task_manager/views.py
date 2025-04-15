from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView,
                                       UpdateView)
from django.views.generic.list import ListView

from task_manager.forms import WorkerCreationForm, TaskForm
from task_manager.models import Worker, Task, TaskType, Tag, Team, Project


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "task_manager/worker_detail.html"
    context_object_name = "worker"

class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "task_manager/worker_form.html"

    def get_success_url(self):
        return reverse("task_manager:worker-login")


class WorkerLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse("task_manager:worker-detail", kwargs={"pk": self.request.user.pk})


class WorkerLogoutView(LogoutView):
    next_page = reverse_lazy("task_manager:worker-login")
    template_name = "registration/logged_out.html"

class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    fields = ("first_name", "last_name", "email", "position", "team")
    template_name = "task_manager/worker_form.html"

    def get_success_url(self):
        return reverse("task_manager:worker-detail", kwargs={"pk": self.request.user.pk})


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Worker
    template_name = "task_manager/worker_confirm_delete.html"
    success_url = reverse_lazy("task_manager:index")


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_form.html"
    success_url = reverse_lazy("task_manager:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.assignees.add(self.request.user)
        return response


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_form.html"
    success_url = reverse_lazy("task_manager:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        if not self.object.assignees.filter(pk=self.request.user.pk).exists():
            self.object.assignees.add(self.request.user)
        return response


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task_manager/task_confirm_delete.html"
    success_url = reverse_lazy("task_manager:index")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_manager/index.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-create")


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = "__all__"
    template_name = "task_manager/tag_form.html"
    success_url = reverse_lazy("task_manager:task-create")


class CreateTeamView(LoginRequiredMixin, CreateView):
    model = Team
    fields = "__all__"
    template_name = "task_manager/team_form.html"
    success_url = reverse_lazy("task_manager:team-list")


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "task_manager/team_list.html"


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "task_manager/team_detail.html"


class JoinTeamView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Team, pk=kwargs.get("pk"))
        team.workers.add(request.user)
        return redirect("task_manager:team-detail", pk=team.pk)


class LeaveTeamView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Team, pk=kwargs["pk"])
        team.workers.remove(request.user)
        return redirect("task_manager:team-detail", pk=team.pk)


class ProjectListView(ListView):
    model = Project
    template_name = "task_manager/project_list.html"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "task_manager/project_detail.html"


class ProjectCreateView(CreateView):
    model = Project
    fields = ["name", "teams"]
    template_name = "task_manager/project_form.html"
    success_url = reverse_lazy("task_manager:project-list")


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ["name", "teams"]
    template_name = "task_manager/project_form.html"
    success_url = reverse_lazy("task_manager:project-list")


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "task_manager/project_confirm_delete.html"
    success_url = reverse_lazy("task_manager:project-list")
