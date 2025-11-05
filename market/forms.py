# market/forms.py
from datetime import datetime

from django import forms
from django.forms import inlineformset_factory

from .models import Vehicle, VehicleImage
from .utils.images import validate_image


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "brand", "model", "year",
            "mileage", "price",
            "city", "state",
            "description",
        ]
        labels = {
            "brand": "Marca",
            "model": "Modelo",
            "year": "Ano",
            "mileage": "Quilometragem (km)",
            "price": "Preço (R$)",
            "city": "Cidade",
            "state": "UF",
            "description": "Descrição",
        }
        help_texts = {
            "mileage": "Informe somente números (km).",
            "price": "Use somente números. Ex.: 59990",
        }
        widgets = {
            "brand": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Ex.: Chevrolet"
            }),
            "model": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Ex.: Onix 1.0"
            }),
            "year": forms.NumberInput(attrs={
                "class": "form-control", "min": 1990, "max": datetime.now().year + 1
            }),
            "mileage": forms.NumberInput(attrs={
                "class": "form-control", "min": 0, "step": 1000
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control", "min": 0, "step": 100
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Sua cidade"
            }),
            "state": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={
                "class": "form-control", "rows": 4,
                "placeholder": "Destaques e observações do veículo"
            }),
        }


class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ["image", "is_cover"]

    def clean_image(self):
        f = self.cleaned_data.get("image")
        if f:
            validate_image(f)  # valida tipo, tamanho e resolução
        return f


# Formset de imagens vinculado ao Vehicle
VehicleImageFormSet = inlineformset_factory(
    Vehicle,
    VehicleImage,
    form=VehicleImageForm,     # usa o form com a validação embutida
    fields=["image", "is_cover"],
    extra=6,
    can_delete=True,
)
