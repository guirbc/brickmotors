from django.contrib import admin
from .models import Vehicle, VehiclePhoto

class VehiclePhotoInline(admin.TabularInline):
    model = VehiclePhoto
    extra = 1

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("id","brand","model","year","city","price","ad_type","is_featured")
    list_filter  = ("ad_type","city","brand","year","is_featured")
    search_fields= ("brand","model","city","title")
    inlines = [VehiclePhotoInline]

# Register your models here.
