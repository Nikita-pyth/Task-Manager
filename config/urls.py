from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls", namespace="tasks")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("teams/", include("teams.urls", namespace="teams")),
    path("projects/", include("projects.urls", namespace="projects")),
    path("positions/", include("positions.urls", namespace="positions")),
]
