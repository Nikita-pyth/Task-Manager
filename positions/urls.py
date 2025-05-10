from django.urls import path
from . import views

app_name = "positions"

urlpatterns = [
    path("create/", views.PositionCreateView.as_view(), name="create"),
]
