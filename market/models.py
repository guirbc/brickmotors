from django.db import models
from django.conf import settings
from django.utils.text import slugify

AD_TYPES = (("normal","Normal"), ("repasse","Repasse"))

class Vehicle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    brand = models.CharField(max_length=60)
    model = models.CharField(max_length=60)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField(default=0)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2, default="SC")
    ad_type = models.CharField(max_length=10, choices=AD_TYPES, default="normal")
    is_drivable = models.BooleanField(default=True)
    has_document = models.BooleanField(default=True)
    issues = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    featured_until = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def save(self,*a,**kw):
        if not self.slug:
            self.slug = slugify(f"{self.brand} {self.model} {self.year}")[:170]
        super().save(*a,**kw)
    def __str__(self): return f"{self.brand} {self.model} {self.year}"

class VehiclePhoto(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="vehicles/")
    order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["order","id"]

# Create your models here.
