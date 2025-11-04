from django.contrib import admin
from .models import Vehicle, VehicleImage

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 0

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("title","brand","model","year","price","owner","is_published")
    list_filter  = ("brand","year","is_published","repass")
    search_fields = ("title","brand","model","city","state")
    inlines = [VehicleImageInline]

@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ("vehicle","order")
