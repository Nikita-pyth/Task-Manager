from django.urls import path
from teams import views

app_name = "teams"

urlpatterns = [
    path("", views.TeamListView.as_view(), name="list"),
    path("create/", views.CreateTeamView.as_view(), name="create"),
    path("<int:pk>/", views.TeamDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.UpdateTeamView.as_view(), name="update"),
    path("<int:pk>/delete/", views.TeamDeleteView.as_view(), name="delete"),
    path("<int:pk>/join/", views.JoinTeamView.as_view(), name="join"),
    path("<int:pk>/leave/", views.LeaveTeamView.as_view(), name="leave"),
]
