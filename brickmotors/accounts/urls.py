from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import SignUpView, ActivateAccountView, ResendActivationView

app_name = "accounts"

urlpatterns = [
    # Todas as URLs padrão: login, logout, password_reset, etc.
    path("", include("django.contrib.auth.urls")),  # <- login/logout/etc

    # Rotas da sua conta:
    path("signup/", SignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
    path("resend-activation/", ResendActivationView.as_view(), name="resend_activation"),
]

