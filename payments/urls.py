from django.urls import path
from . import views

app_name = "payments"
urlpatterns = [
    path("destacar/<int:pk>/", views.highlight_vehicle, name="highlight"),
    path("webhook/<str:secret>/", views.webhook, name="webhook"),
    path("sucesso/", views.success, name="success"),
    path("falha/", views.failure, name="failure"),
    path("pendente/", views.pending, name="pending"),
]
