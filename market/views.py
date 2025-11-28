# market/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from .models import Vehicle
from .forms import VehicleForm, VehicleImageFormSet


def home(request):
    vehicles = (
        Vehicle.objects
        .select_related("owner")
        .prefetch_related("images")
        .order_by("-created_at")
    )
    return render(request, "home.html", {"vehicles": vehicles[:12]})


class MyVehiclesView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = "market/my_vehicles.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        return (
            Vehicle.objects
            .filter(owner=self.request.user)
            .prefetch_related("images")
            .order_by("-created_at")
        )


class VehicleCreateView(LoginRequiredMixin, CreateView):
    template_name = "market/vehicle_form.html"
    form_class = VehicleForm
    success_url = reverse_lazy("market:my_vehicles")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["images_formset"] = VehicleImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            ctx["images_formset"] = VehicleImageFormSet()
        return ctx

    def form_valid(self, form):
        images_formset = VehicleImageFormSet(
            self.request.POST, self.request.FILES
        )

        with transaction.atomic():
            form.instance.owner = self.request.user
            self.object = form.save()

            # agora que há veículo salvo, ligamos o formset
            images_formset.instance = self.object
            if images_formset.is_valid():
                images_formset.save()
                messages.success(self.request, "Anúncio criado com sucesso!")
                return redirect(self.success_url)

        # se o formset não for válido, re-renderiza com erros
        return self.render_to_response(
            self.get_context_data(form=form, images_formset=images_formset)
        )


class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "market/vehicle_edit.html"
    success_url = reverse_lazy("market:my_vehicles")

    def test_func(self):
        return self.get_object().owner_id == self.request.user.pk

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["images_formset"] = VehicleImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            ctx["images_formset"] = VehicleImageFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        images_formset = VehicleImageFormSet(
            self.request.POST, self.request.FILES, instance=self.object
        )
        if images_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                images_formset.save()
            messages.success(self.request, "Anúncio atualizado com sucesso!")
            return redirect(self.success_url)

        return self.render_to_response(
            self.get_context_data(form=form, images_formset=images_formset)
        )


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = "market/vehicle_detail.html"
    context_object_name = "vehicle"

def search(request):
    vehicles = (
        Vehicle.objects
        .select_related("owner")
        .prefetch_related("images")
        .order_by("-created_at")
    )

    q = (request.GET.get("q") or "").strip()
    tipo = request.GET.get("tipo")       # carro / moto
    cond = request.GET.get("cond")       # novo / usado
    vistoriado = request.GET.get("vistoriado")  # "1" se marcado

    # filtro por texto (campo de busca)
    if q:
        vehicles = vehicles.filter(
            Q(make__icontains=q) |
            Q(model__icontains=q) |
            Q(city__icontains=q) |
            Q(description__icontains=q)
        )

    # tenta aplicar filtros extras só se o campo existir no model
    field_names = {f.name for f in Vehicle._meta.get_fields()}

    # tipo: carro/moto
    if tipo:
        if "tipo" in field_names:
            vehicles = vehicles.filter(tipo=tipo)
        elif "vehicle_type" in field_names:
            vehicles = vehicles.filter(vehicle_type=tipo)

    # condição: novo/usado
    if cond:
        if "condition" in field_names:
            vehicles = vehicles.filter(condition=cond)
        elif "is_new" in field_names:
            is_new = (cond == "novo")
            vehicles = vehicles.filter(is_new=is_new)

    # vistoriado
    if vistoriado:
        if "is_certified" in field_names:
            vehicles = vehicles.filter(is_certified=True)
        elif "vistoriado" in field_names:
            vehicles = vehicles.filter(vistoriado=True)

    context = {
        "vehicles": vehicles,
        "q": q,
        "tipo": tipo,
        "cond": cond,
        "vistoriado": vistoriado,
    }
    return render(request, "market/search_results.html", context)
