from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls.base import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.forms import WorkerCreationForm
from task_manager.models import Worker


class WorkerDetailView(DetailView):
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


class WorkerUpdateView(UpdateView):
    model = Worker
    fields = ("first_name", "last_name", "email", "position", "team")
    template_name = "task_manager/worker_form.html"

    def get_success_url(self):
        return reverse("task_manager:worker-detail", kwargs={"pk": self.request.user.pk})


class WorkerDeleteView(DeleteView):
    model = Worker
    template_name = "task_manager/worker_confirm_delete.html"
    success_url = reverse_lazy("task_manager:index")


