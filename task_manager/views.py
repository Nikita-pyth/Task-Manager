from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView,
                                       UpdateView)
from django.views.generic.list import ListView

from task_manager.forms import WorkerCreationForm, TaskForm, ProjectForm, ProjectScopedTaskForm
from task_manager.models import Worker, Task, TaskType, Tag, Team, Project, Position


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
    fields = ("first_name", "last_name", "email", "team", "position")
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
        self.object.assignees.set([self.request.user])
        return response


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_tasks = Task.objects.filter(assignees=self.request.user)

        context["personal_tasks"] = user_tasks.filter(project__isnull=True)
        context["project_tasks"] = user_tasks.filter(project__isnull=False)
        return context


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-create")


class ChangeTaskStatus(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])

        if request.user in task.assignees.all():
            task.is_completed = not task.is_completed
            task.save()

        return redirect(request.META.get("HTTP_REFERER", "task_manager:index"))


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = "__all__"
    template_name = "task_manager/tag_form.html"
    success_url = reverse_lazy("task_manager:task-create")


class CreateTeamView(LoginRequiredMixin, CreateView):
    model = Team
    fields = ["name",]
    template_name = "task_manager/team_form.html"
    success_url = reverse_lazy("task_manager:team-list")

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
    template_name = "task_manager/team_list.html"


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "task_manager/team_detail.html"


class UpdateTeamView(LoginRequiredMixin, UpdateView):
    model = Team
    fields = ["name", "admins"]
    template_name = "task_manager/team_form.html"
    success_url = reverse_lazy("task_manager:team-list")

    def dispatch(self, request, *args, **kwargs):
        team = self.get_object()
        if request.user not in team.admins.all():
            return HttpResponseForbidden("You are not allowed to update this team.")
        return super().dispatch(request, *args, **kwargs)

class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = "task_manager/team_confirm_delete.html"
    success_url = reverse_lazy("task_manager:team-list")


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


class ProjectListView(LoginRequiredMixin,ListView):
    model = Project
    template_name = "task_manager/project_list.html"


class ProjectDetailView(LoginRequiredMixin,DetailView):
    model = Project
    template_name = "task_manager/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["admin_projects"] = Project.objects.filter(teams__admins=user).distinct()
        print(context["admin_projects"])
        return context

class ProjectCreateView(LoginRequiredMixin,CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "task_manager/project_form.html"
    success_url = reverse_lazy("task_manager:project-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProjectUpdateView(LoginRequiredMixin,UpdateView):
    model = Project
    fields = ["name", "teams"]
    template_name = "task_manager/project_form.html"
    success_url = reverse_lazy("task_manager:project-list")

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user not in project.admins.all():
            return HttpResponseForbidden("You are not allowed to edit this project.")
        return super().dispatch(request, *args, **kwargs)


class ProjectDeleteView(LoginRequiredMixin,DeleteView):
    model = Project
    template_name = "task_manager/project_confirm_delete.html"
    success_url = reverse_lazy("task_manager:project-list")


class ProjectTaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = ProjectScopedTaskForm
    template_name = "task_manager/task_form.html"

    def get_success_url(self):
        return reverse_lazy("task_manager:project-detail", kwargs={"pk": self.project.pk})

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
        response = super().form_valid(form)
        self.object.assignees.set([self.request.user])
        return response


class PositionCreateView(CreateView):
    model = Position
    fields = "__all__"
    template_name = "task_manager/position_form.html"

    def get_success_url(self):
        return reverse_lazy("task_manager:worker-update", kwargs={"pk": self.request.user.pk})
