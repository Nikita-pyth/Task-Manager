from django.urls import path
from tasks import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="index"),
    path("create/", views.TaskCreateView.as_view(), name="create"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="delete"),
    path("<int:pk>/toggle_status/", views.ChangeTaskStatus.as_view(), name="toggle-status"),
    path("tasktype/create/", views.TaskTypeCreateView.as_view(), name="tasktype-create"),
    path("tag/create/", views.TagCreateView.as_view(), name="tag-create"),
]
