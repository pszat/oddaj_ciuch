from mysite import models
from django import forms
from django.core.validators import ValidationError
from django.contrib.auth import password_validation

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
        # cleaned_data = super(RegistrationForm).clean()
        password = self.cleaned_data.get("password")
        check_password = self.cleaned_data.get("check_password")
        username = self.cleaned_data.get('email')
        if password != check_password:
            raise ValidationError("Oba hasła muszę być identyczne")
        if models.User.objects.filter(username=username).count() > 0:
            raise ValidationError("Użytkownik z podanym adresem email już istnieje")
        password_validation.validate_password(password)
