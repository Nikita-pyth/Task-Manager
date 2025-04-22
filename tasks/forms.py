from django import forms
from django.utils.timezone import now
from tasks.models import Task


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "priority", "deadline", "type", "tags"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={
                "type": "date",
                "class": "form-control",
                "min": now().date().isoformat(),
            }),
        }


class TaskUpdateForm(TaskCreateForm):
    class Meta(TaskCreateForm.Meta):
        fields = TaskCreateForm.Meta.fields + ["is_completed"]
