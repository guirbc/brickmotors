from django.urls import path
from . import views

app_name = "market"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("busca/", views.VehicleListView.as_view(), name="busca"),
    path("repasses/", views.RepassesListView.as_view(), name="repasses"),
    path("veiculo/<int:pk>-<slug:slug>/", views.VehicleDetailView.as_view(), name="veiculo"),
]
