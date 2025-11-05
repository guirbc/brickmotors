from django.urls import path
from . import views, views_catalog

app_name = "market"

urlpatterns = [
    path("", views.home, name="home"),
    path("meus-anuncios/", views.MyVehiclesView.as_view(), name="my_vehicles"),
    path("anunciar/", views.VehicleCreateView.as_view(), name="vehicle_create"),
    path("editar/<int:pk>/", views.VehicleUpdateView.as_view(), name="vehicle_update"),
    path("<int:pk>/", views.VehicleDetailView.as_view(), name="vehicle_detail"),

    # APIs de auto-complete:
    path("api/makes/", views_catalog.api_makes, name="api_makes"),
    path("api/models/", views_catalog.api_models, name="api_models"),
    path("api/makes/", views_catalog.api_makes, name="api_makes"),
    path("api/models/", views_catalog.api_models, name="api_models")
]
