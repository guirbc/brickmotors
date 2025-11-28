# brickmotors/accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignUpView, ActivateAccountView, ResendActivationView

app_name = "accounts"

urlpatterns = [
    # LOGIN
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),

    # LOGOUT
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # SIGNUP / CADASTRO
    path("signup/", SignUpView.as_view(), name="signup"),

    # ATIVAÇÃO DE CONTA POR E-MAIL
    path(
        "activate/<uidb64>/<token>/",
        ActivateAccountView.as_view(),
        name="activate",
    ),

    # REENVIAR LINK DE ATIVAÇÃO
    path(
        "resend-activation/",
        ResendActivationView.as_view(),
        name="resend",
    ),

    # ====== RESET DE SENHA ======
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
