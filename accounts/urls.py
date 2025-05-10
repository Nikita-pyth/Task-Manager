from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("create/", views.WorkerCreateView.as_view(), name="create"),
    path("login/", views.WorkerLoginView.as_view(), name="login"),
    path("logout/", views.WorkerLogoutView.as_view(), name="logout"),
    path("<int:pk>/", views.WorkerDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.WorkerUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.WorkerDeleteView.as_view(), name="delete"),
]
