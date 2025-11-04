from django.urls import path
from . import views

app_name = "market"

urlpatterns = [
    path("", views.home, name="home"),             # <- nova home
    path("busca/", views.CatalogView.as_view(), name="catalog"),
    path("anunciar/", views.vehicle_create, name="vehicle_create"),
    path("meus-anuncios/", views.my_vehicles, name="my_vehicles"),
    path("editar/<slug:slug>/", views.vehicle_edit, name="vehicle_edit"),
    path("<slug:slug>/", views.vehicle_detail, name="vehicle_detail"),
]
