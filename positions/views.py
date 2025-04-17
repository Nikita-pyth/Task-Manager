from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView

from positions.models import Position


class PositionCreateView(CreateView):
    model = Position
    fields = "__all__"
    template_name = "positions/position_form.html"

    def get_success_url(self):
        return reverse_lazy("accounts:update", kwargs={"pk": self.request.user.pk})