from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Vamos confirmar seu e-mail.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # estiliza inputs (sem precisar de filter add_class)
        for f in self.fields.values():
            f.widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email
