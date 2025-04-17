from django.contrib.auth.forms import UserCreationForm

from accounts.models import Worker


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email")