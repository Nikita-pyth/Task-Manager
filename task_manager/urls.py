from django.urls.conf import path

import task_manager.views

urlpatterns = [
    path("", task_manager.views.TaskListView.as_view(), name="index"),
    path("accounts/create", task_manager.views.WorkerCreateView.as_view(), name="worker-create"),
    path("accounts/login", task_manager.views.WorkerLoginView.as_view(), name="worker-login"),
    path("accounts/<int:pk>/update/", task_manager.views.WorkerUpdateView.as_view(), name="worker-update"),
    path("accounts/<int:pk>/delete/", task_manager.views.WorkerDeleteView.as_view(), name="worker-delete"),
    path("accounts/<int:pk>/", task_manager.views.WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/create/", task_manager.views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", task_manager.views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", task_manager.views.TaskDeleteView.as_view(), name="task-delete"),

]

app_name = "task_manager"
