from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Worker
from accounts.forms import WorkerCreationForm

class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "accounts/worker_detail.html"
    context_object_name = "worker"

class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "accounts/worker_form.html"

    def get_success_url(self):
        return reverse("accounts:login")

class WorkerLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse("accounts:detail", kwargs={"pk": self.request.user.pk})

class WorkerLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")
    template_name = "accounts/logged_out.html"

class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    fields = ("first_name", "last_name", "email", "team", "position")
    template_name = "accounts/worker_form.html"

    def get_success_url(self):
        return reverse("accounts:detail", kwargs={"pk": self.request.user.pk})

class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Worker
    template_name = "accounts/worker_confirm_delete.html"
    success_url = reverse_lazy("accounts:login")
