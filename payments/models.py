from django.db import models
from django.conf import settings
from market.models import Vehicle

class Order(models.Model):
    STATUS = (("pending","Pendente"),("approved","Aprovado"),("rejected","Rejeitado"),("cancelled","Cancelado"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS, default="pending")
    mp_preference_id = models.CharField(max_length=80, blank=True)
    mp_payment_id = models.CharField(max_length=80, blank=True)
    external_reference = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Order #{self.pk} - {self.status}"

# Create your models here.
