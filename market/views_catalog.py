# market/views_catalog.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import CarMake, CarModel

@require_GET
def api_makes(request):
    q = (request.GET.get("q") or "").strip()
    qs = CarMake.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    data = [{"id": m.pk, "name": m.name} for m in qs.order_by("name")[:20]]
    return JsonResponse({"results": data})

@require_GET
def api_models(request):
    make_id = request.GET.get("make_id")
    q = (request.GET.get("q") or "").strip()
    qs = CarModel.objects.all()
    if make_id:
        qs = qs.filter(make_id=make_id)
    if q:
        qs = qs.filter(name__icontains=q)
    data = [{"id": m.pk, "name": m.name} for m in qs.order_by("name")[:30]]
    return JsonResponse({"results": data})
