from django import forms

from order.models import OrderAddressDB


class ShippingForm(forms.ModelForm):
    """Адреса доставки"""

    class Meta:
        model = OrderAddressDB
        fields = ("index", "city", "state", "street")
        widgets = {
            "index": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "01008"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Київ"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Київська область"}
            ),
            "street": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Вулиця/Будинок/Квартира...",
                }
            ),
        }
