from django.urls.conf import path

import task_manager.views

urlpatterns = [
    path("", task_manager.views.TaskListView.as_view(), name="index"),
    path("accounts/create/", task_manager.views.WorkerCreateView.as_view(), name="worker-create"),
    path("accounts/login/", task_manager.views.WorkerLoginView.as_view(), name="worker-login"),
    path("accounts/logout/", task_manager.views.WorkerLogoutView.as_view(), name="worker-logout"),
    path("accounts/<int:pk>/update/", task_manager.views.WorkerUpdateView.as_view(), name="worker-update"),
    path("accounts/<int:pk>/delete/", task_manager.views.WorkerDeleteView.as_view(), name="worker-delete"),
    path("accounts/<int:pk>/", task_manager.views.WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/create/", task_manager.views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", task_manager.views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/", task_manager.views.TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/delete/", task_manager.views.TaskDeleteView.as_view(), name="task-delete"),
    # urls.py
    path("tasktype/create/", task_manager.views.TaskTypeCreateView.as_view(), name="tasktype-create"),
    path("tag/create/", task_manager.views.TagCreateView.as_view(), name="tag-create"),
    path("teams/", task_manager.views.TeamListView.as_view(), name="team-list"),
    path("teams/create/", task_manager.views.CreateTeamView.as_view(), name="team-create"),
    path("teams/<int:pk>/update", task_manager.views.UpdateTeamView.as_view(), name="team-update"),
    path("teams/<int:pk>/", task_manager.views.TeamDetailView.as_view(), name="team-detail"),
    path("teams/<int:pk>/delete", task_manager.views.TeamDeleteView.as_view(), name="team-delete"),
    path("teams/<int:pk>/join/", task_manager.views.JoinTeamView.as_view(), name="team-join"),
    path("teams/<int:pk>/leave/", task_manager.views.LeaveTeamView.as_view(), name="team-leave"),
    path("projects/", task_manager.views.ProjectListView.as_view(), name="project-list"),
    path("projects/create/", task_manager.views.ProjectCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>/", task_manager.views.ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<int:pk>/update/", task_manager.views.ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<int:pk>/delete/", task_manager.views.ProjectDeleteView.as_view(), name="project-delete"),
    path("projects/<int:pk>/create_task/", task_manager.views.ProjectTaskCreateView.as_view(),
         name="project-task-create"),
    path("tasks/<int:pk>/toggle_status/", task_manager.views.ChangeTaskStatus.as_view(), name="task-toggle-status"),

]

app_name = "task_manager"
