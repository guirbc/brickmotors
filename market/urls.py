from django.urls import path
from . import views

app_name = "market"

urlpatterns = [
    path("", views.home, name="home"),
    path("meus-anuncios/", views.MyVehiclesView.as_view(), name="my_vehicles"),
    path("anunciar/", views.VehicleCreateView.as_view(), name="vehicle_create"),
    path("editar/<int:pk>/", views.VehicleUpdateView.as_view(), name="vehicle_update"),
    path("<int:pk>/", views.VehicleDetailView.as_view(), name="vehicle_detail"),

    # <<< nova rota >>>
    path("busca/", views.search, name="search"),

    # se já tiver as APIs, deixa como estão
    # path("api/makes/", views.api_makes, name="api_makes"),
    # path("api/models/", views.api_models, name="api_models"),
]
