# market/admin.py
from django.contrib import admin
from .models import Make, MakeModel, Vehicle, VehicleImage

@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]

@admin.register(MakeModel)
class MakeModelAdmin(admin.ModelAdmin):
    search_fields = ["name", "make__name"]
    list_display = ["name", "make"]
    list_filter = ["make"]

# (deixa os admins existentes do Vehicle/VehicleImage como já estavam)
