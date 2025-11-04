from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from datetime import timedelta
from market.models import Vehicle
from .models import Order
import mercadopago, json

mp = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

def highlight_vehicle(request, pk):
    v = get_object_or_404(Vehicle, pk=pk)
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=" + request.path)
    order = Order.objects.create(user=request.user, vehicle=v, amount=Decimal("29.90"), status="pending")
    pref = {
        "items":[{"title":f"Destaque #{v.pk}","quantity":1,"unit_price":float(order.amount),"currency_id":"BRL"}],
        "back_urls":{
            "success": request.build_absolute_uri("/pagamentos/sucesso/"),
            "failure": request.build_absolute_uri("/pagamentos/falha/"),
            "pending": request.build_absolute_uri("/pagamentos/pendente/"),
        },
        "auto_return":"approved",
        "notification_url": request.build_absolute_uri(f"/pagamentos/webhook/{settings.MP_WEBHOOK_SECRET}/"),
        "external_reference": str(order.pk),
    }
    res = mp.preference().create(pref)
    order.mp_preference_id = res["response"]["id"]
    order.external_reference = str(order.pk)
    order.save()
    return redirect(res["response"]["init_point"])

@csrf_exempt
def webhook(request, secret):
    if secret != settings.MP_WEBHOOK_SECRET:
        return HttpResponseForbidden()
    try:
        payload = json.loads(request.body or "{}")
        if payload.get("type") == "payment":
            pid = payload["data"]["id"]
            payment = mp.payment().get(pid)["response"]
#            order = Order.objects.get(id=int(payment["external_reference"]))
            order = Order.objects.get(pk=int(payment["external_reference"]))
            st = payment["status"]
            order.status = "approved" if st == "approved" else "pending" if st == "in_process" else "rejected"
            order.mp_payment_id = str(pid)
            order.save()
            if order.status == "approved" and order.vehicle:
                order.vehicle.is_featured = True
                order.vehicle.featured_until = timezone.now() + timedelta(days=30)
                order.vehicle.save()
    except Exception:
        pass
    return HttpResponse(status=200)

def success(request): return render(request,"payments/success.html")
def failure(request): return render(request,"payments/failure.html")
def pending(request): return render(request,"payments/pending.html")

# Create your views here.
