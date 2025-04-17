from django import forms
from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "priority", "deadline", "type", "tags", "is_completed"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={
                "type": "date",
                "class": "form-control",
            }),
        }
