
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls.base import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView,
                                       UpdateView)
from django.views.generic.list import ListView

from task_manager.forms import WorkerCreationForm, TaskForm
from task_manager.models import Worker, Task


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "task_manager/worker_detail.html"
    context_object_name = "worker"

class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "task_manager/worker_form.html"
    success_url = reverse_lazy("task_manager:worker-detail")


class WorkerLoginView(LoginView):
    template_name = "task_manager/worker_login.html"

    def get_success_url(self):
        return reverse("task_manager:worker-detail", kwargs={"pk": self.request.user.pk})


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
        self.object.assignees.add(self.request.user)  # Auto-assign creator
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