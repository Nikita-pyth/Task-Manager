from django import forms
from django.contrib.auth.forms import UserCreationForm
from task_manager.models import Worker, Task, Team, Project


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "priority", "deadline", "type", "is_completed"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={
                "type": "date",
                "class": "form-control",
            }),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "teams"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")  # pass user manually
        super().__init__(*args, **kwargs)

        admin_teams = Team.objects.filter(admins=user)

        if admin_teams.exists():
            self.fields["teams"].queryset = admin_teams
        else:
            self.fields["teams"].queryset = Team.objects.none()
            self.fields["teams"].help_text = (
                "You are not an admin in any team. "
                "<a href='/teams/create/'>Create a new team</a>."
            )


class ProjectScopedTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["project"]
        widgets = {
            "deadline": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        team_members = kwargs.pop("team_members", None)
        super().__init__(*args, **kwargs)

        if team_members:
            self.fields["assignees"].queryset = team_members
