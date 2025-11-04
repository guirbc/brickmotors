# accounts/utils_email.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_activation_email(user, activation_link, expiry_minutes=30):
    subject = "Ative sua conta · BrickMotors"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    ctx = {
        "user": user,
        "activation_link": activation_link,
        "expiry_minutes": expiry_minutes,
    }

    html_body = render_to_string("emails/activation.html", ctx)
    txt_body  = render_to_string("emails/activation.txt", ctx)

    msg = EmailMultiAlternatives(subject, txt_body, from_email, to)
    msg.attach_alternative(html_body, "text/html")

    # (opcional) cabeçalhos que ajudam reputação/entendimento do provedor
    msg.extra_headers = {
        "X-Entity-Ref-ID": str(user.pk),  # correlação
    }

    msg.send()
