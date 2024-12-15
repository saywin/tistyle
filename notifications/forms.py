from django import forms

from notifications.models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["email", "name", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше ім'я"}),
            "email": forms.EmailInput(attrs={"placeholder": "Ваш email"}),
            "message": forms.Textarea(attrs={"placeholder": "Повідомлення"}),
        }
