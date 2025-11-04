from pathlib import Path
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from uuid import uuid4
from pathlib import Path

FUEL_CHOICES = [
    ("flex", "Flex"),
    ("gasolina", "Gasolina"),
    ("etanol", "Etanol"),
    ("diesel", "Diesel"),
    ("eletrico", "Elétrico"),
    ("hibrido", "Híbrido"),
]

GEAR_CHOICES = [
    ("manual", "Manual"),
    ("auto", "Automático"),
    ("cvt", "CVT"),
]


def vehicle_image_path(instance, filename):
    ext = Path(filename).suffix.lower()

    # tenta pegar o PK via o FK "vehicle"
    vehicle_obj = getattr(instance, "vehicle", None)
    vid = getattr(vehicle_obj, "pk", None)

    # se ainda não existir (ex.: criação antes de salvar o veículo), usa um UUID temporário
    if not vid:
        vid = f"temp-{uuid4().hex}"

    return f"vehicles/{vid}/{uuid4().hex}{ext}"


class Vehicle(models.Model):
    # ...
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vehicles",
    )
    title       = models.CharField("Título curto", max_length=120)
    brand       = models.CharField("Marca", max_length=50)
    model       = models.CharField("Modelo", max_length=80)
    version     = models.CharField("Versão", max_length=80, blank=True)
    year        = models.PositiveSmallIntegerField("Ano")
    mileage     = models.PositiveIntegerField("Quilometragem (km)")
    price       = models.DecimalField("Preço", max_digits=12, decimal_places=2)
    fuel        = models.CharField("Combustível", max_length=12, choices=FUEL_CHOICES, default="flex")
    gearbox     = models.CharField("Câmbio", max_length=10, choices=GEAR_CHOICES, default="manual")
    body_type   = models.CharField("Carroceria", max_length=30, blank=True)  # hatch, sedan, suv...
    color       = models.CharField("Cor", max_length=30, blank=True)

    city        = models.CharField("Cidade", max_length=60)
    state       = models.CharField("UF", max_length=2)

    repass      = models.BooleanField("É repasse?", default=False)  # extra, não é destaque
    is_published= models.BooleanField("Publicado", default=True)

    slug        = models.SlugField(unique=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes  = [models.Index(fields=["slug"]), models.Index(fields=["brand","model","year"])]

    def __str__(self):
        return f"{self.title} - {self.city}/{self.state}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.brand}-{self.model}-{self.year}-{uuid4().hex[:6]}"
            self.slug = slugify(base)
        super().save(*args, **kwargs)

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name="images", on_delete=models.CASCADE)
    image   = models.ImageField(upload_to=vehicle_image_path)
    order   = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Foto {self.order} de {self.vehicle_id}" # type: ignore
