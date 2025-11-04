from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView
from django.core.mail import EmailMultiAlternatives


from .forms import SignUpForm

User = get_user_model()


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # só entra após confirmar o e-mail
        user.email = form.cleaned_data["email"].lower()
        user.save()

        self._send_activation_email(user)

        messages.success(self.request, "Enviamos um link de confirmação para o seu e-mail.")
        return redirect("accounts:login")

    def _send_activation_email(self, user):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activate_url = self.request.build_absolute_uri(
            reverse("accounts:activate", args=[uidb64, token])
        )

        ctx = {
            "user": user,
            "activate_url": activate_url,  # <- nome padronizado com os templates
        }

        subject = "Confirme seu e-mail — BrickMotors"
        text_body = render_to_string("emails/activation_email.txt", ctx)
        html_body = render_to_string("emails/activation_email.html", ctx)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,  # fallback texto puro
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Conta confirmada! Agora você já pode entrar.")
            return redirect("accounts:login")

        messages.error(request, "Link inválido ou expirado. Peça um novo link.")
        return redirect("accounts:resend")


class ResendActivationView(View):
    template_name = "registration/resend_activation.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = (request.POST.get("email") or "").lower()

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # Resposta genérica para não vazar se o e-mail existe
            messages.info(request, "Se houver uma conta com este e-mail, enviamos um novo link.")
            return redirect("accounts:login")

        if user.is_active:
            messages.info(request, "Esta conta já está ativa. Pode fazer login.")
            return redirect("accounts:login")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = request.build_absolute_uri(reverse("accounts:activate", args=[uid, token]))

        subject = "Confirme seu e-mail — BrickMotors"
        message = render_to_string("emails/activation_email.txt", {"user": user, "url": url})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        messages.success(request, "Se houver uma conta com este e-mail, enviamos um novo link.")
        return redirect("accounts:login")
