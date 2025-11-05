# market/models.py (trecho relevante)

from django.conf import settings
from django.db import models
from .utils.images import validate_image  # se você estiver validando
from django.core.validators import MinValueValidator

# choices de UFs do Brasil (pode ajustar/encurtar se quiser)
UF_CHOICES = (
    ("AC", "AC"), ("AL", "AL"), ("AP", "AP"), ("AM", "AM"),
    ("BA", "BA"), ("CE", "CE"), ("DF", "DF"), ("ES", "ES"),
    ("GO", "GO"), ("MA", "MA"), ("MT", "MT"), ("MS", "MS"),
    ("MG", "MG"), ("PA", "PA"), ("PB", "PB"), ("PR", "PR"),
    ("PE", "PE"), ("PI", "PI"), ("RJ", "RJ"), ("RN", "RN"),
    ("RS", "RS"), ("RO", "RO"), ("RR", "RR"), ("SC", "SC"),
    ("SP", "SP"), ("SE", "SE"), ("TO", "TO"),
)


def vehicle_image_path(instance, filename):
    return f"vehicles/{instance.vehicle_id}/{filename}"

class Vehicle(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vehicles",
    )
    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=120)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
     # NOVOS CAMPOS
    mileage = models.PositiveIntegerField(
        "Quilometragem (km)", default=0,
        validators=[MinValueValidator(0)], db_index=True
    )
    price = models.PositiveIntegerField("Preço (R$)", validators=[MinValueValidator(0)], db_index=True)
    mileage = models.PositiveIntegerField("Quilometragem (km)", validators=[MinValueValidator(0)], db_index=True)

    city = models.CharField("Cidade", max_length=80, db_index=True)
    state = models.CharField("UF", max_length=2, choices=UF_CHOICES, db_index=True)

    description = models.TextField("Descrição", blank=True)  # <= ADICIONE ESTA LINHA

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField("Cidade", max_length=80, db_index=True)
    state = models.CharField("UF", max_length=2, choices=UF_CHOICES, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # … (demais campos que já definimos)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # agora está DENTRO da classe
        return f"{self.brand} {self.model} {self.year}"

    @property
    def title(self):
        # usado apenas para exibição no admin
        return f"{self.brand} {self.model} {self.year}"


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to=vehicle_image_path,
        validators=[validate_image],   # se estiver usando validação
    )
    is_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem (id={self.pk}) de {self.vehicle}"

class Make(models.Model):  # marcas
    name = models.CharField(max_length=80, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MakeModel(models.Model):  # modelos por marca
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=120, db_index=True)

    class Meta:
        unique_together = [("make", "name")]
        ordering = ["name"]

    def __str__(self):
        return f"{self.make.name} {self.name}"

class CarMake(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        ordering = ["name"]
    def __str__(self): return self.name

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=80)
    class Meta:
        ordering = ["name"]
        unique_together = (("make", "name"),)
    def __str__(self): return f"{self.make} {self.name}"
