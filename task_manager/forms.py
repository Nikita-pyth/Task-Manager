from django import forms
from django.contrib.auth.forms import UserCreationForm
from task_manager.models import Worker, Task


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "position", "team")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(attrs={
                "type": "date",
                "class": "form-control",
            }),
        }
