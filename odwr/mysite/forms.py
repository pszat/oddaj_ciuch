from mysite import models
from django import forms
from django.core.validators import ValidationError


class RegistrationForm(forms.ModelForm):

    check_password = forms.CharField(
        max_length=128, required=True, widget=forms.PasswordInput(attrs={"placeholder": "Potwierdź hasło"}),
    )

    class Meta:
        model = models.User
        fields = ["email", "first_name", "last_name", "password"]
        widgets = {
            'password':forms.PasswordInput(attrs={"placeholder": "Hasło"}),
            'email':forms.TextInput(attrs={"placeholder": "Email"}),
            'first_name': forms.TextInput(attrs={"placeholder": "Imię"}),
            'last_name': forms.TextInput(attrs={"placeholder": "Nazwisko"})
        }

    def clean(self):
        cleaned_data = super(self).clean()
        password = cleaned_data.get("password")
        check_password = cleaned_data.get("check_password")
        if password != check_password:
            raise ValidationError("Oba hasła muszę być identyczne")