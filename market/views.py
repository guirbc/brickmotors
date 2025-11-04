from django.views.generic import TemplateView, DetailView
from django_filters.views import FilterView
from django.db.models import Q
import django_filters
from .models import Vehicle

class HomeView(TemplateView):
    template_name = "home.html"

class VehicleFilter(django_filters.FilterSet):
    preco_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    preco_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    q = django_filters.CharFilter(method="filtrar_q", label="Busca")
    class Meta:
        model = Vehicle
        fields = ["brand","city","ad_type","preco_min","preco_max"]
    def filtrar_q(self, qs, name, value):
        return qs.filter(Q(title__icontains=value)|Q(model__icontains=value)|Q(issues__icontains=value))

class VehicleListView(FilterView):
    model = Vehicle
    paginate_by = 12
    filterset_class = VehicleFilter
    template_name = "catalog/index.html"

class RepassesListView(VehicleListView):
    def get_queryset(self):
        return super().get_queryset().filter(ad_type="repasse")

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = "catalog/show.html"

# Create your views here.
