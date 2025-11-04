# market/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Vehicle, VehicleImage

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "title","brand","model","version","year","mileage","price",
            "fuel","gearbox","body_type","color","city","state","repass","is_published"
        ]
        widgets = {
            "title":  forms.TextInput(attrs={"class":"form-control input-pill"}),
            "brand":  forms.TextInput(attrs={"class":"form-control input-pill"}),
            "model":  forms.TextInput(attrs={"class":"form-control input-pill"}),
            "version":forms.TextInput(attrs={"class":"form-control input-pill"}),
            "body_type":forms.TextInput(attrs={"class":"form-control input-pill"}),
            "color":  forms.TextInput(attrs={"class":"form-control input-pill"}),
            "city":   forms.TextInput(attrs={"class":"form-control input-pill"}),
            "state":  forms.TextInput(attrs={"class":"form-control input-pill"}),

            "year":    forms.NumberInput(attrs={"class":"form-control input-pill","min":"1950","max":"2100"}),
            "mileage": forms.NumberInput(attrs={"class":"form-control input-pill","min":"0"}),
            "price":   forms.NumberInput(attrs={"class":"form-control input-pill","step":"0.01","min":"0"}),

            "fuel":    forms.Select(attrs={"class":"form-select input-pill"}),
            "gearbox": forms.Select(attrs={"class":"form-select input-pill"}),

            "repass":       forms.CheckboxInput(attrs={"class":"form-check-input"}),
            "is_published": forms.CheckboxInput(attrs={"class":"form-check-input"}),
        }

VehicleImageFormSet = inlineformset_factory(
    Vehicle, VehicleImage,
    fields=("image","order"),
    extra=6, can_delete=True, max_num=12
)
