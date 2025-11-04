from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django_filters.views import FilterView
import django_filters

from .models import Vehicle
from .forms import VehicleForm, VehicleImageFormSet

# market/views.py (trecho do filtro)
class VehicleFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="search", label="Busca")
    brand = django_filters.CharFilter(lookup_expr="icontains")
    model = django_filters.CharFilter(lookup_expr="icontains")
    year_min = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    year_max = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Vehicle
        fields = ["brand", "model", "fuel", "gearbox", "repass", "city", "state"]  # <- nada de ad_type

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(title__icontains=value) | queryset.filter(model__icontains=value)

class CatalogView(FilterView):
    template_name = "market/catalog.html"
    filterset_class = VehicleFilter
    paginate_by = 24

    def get_queryset(self):
        return Vehicle.objects.filter(is_published=True).select_related("owner").prefetch_related("images")

# ---- privado: CRUD do anunciante
@login_required
def vehicle_create(request):
    v = Vehicle(owner=request.user)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=v)
        formset = VehicleImageFormSet(request.POST, request.FILES, instance=v)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Anúncio criado com sucesso!")
            return redirect("market:my_vehicles")
    else:
        form = VehicleForm(instance=v)
        formset = VehicleImageFormSet(instance=v)
    return render(request, "market/vehicle_form.html", {"form": form, "formset": formset, "title":"Criar anúncio"})

@login_required
def vehicle_edit(request, slug):
    v = get_object_or_404(Vehicle, slug=slug, owner=request.user)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=v)
        formset = VehicleImageFormSet(request.POST, request.FILES, instance=v)
        if form.is_valid() and formset.is_valid():
            form.save(); formset.save()
            messages.success(request, "Anúncio atualizado.")
            return redirect("market:my_vehicles")
    else:
        form = VehicleForm(instance=v)
        formset = VehicleImageFormSet(instance=v)
    return render(request, "market/vehicle_form.html", {"form": form, "formset": formset, "title":"Editar anúncio"})

@login_required
def my_vehicles(request):
    qs = Vehicle.objects.filter(owner=request.user).prefetch_related("images")
    return render(request, "market/my_vehicles.html", {"vehicles": qs})

def vehicle_detail(request, slug):
    v = get_object_or_404(Vehicle, slug=slug, is_published=True)
    return render(request, "market/vehicle_detail.html", {"v": v})

# market/views.py
from django.shortcuts import render

def home(request):
    return render(request, "home.html")  # use seu template com o hero
