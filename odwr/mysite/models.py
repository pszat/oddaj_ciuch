from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=128, unique=True, null=False)


class Institution(models.Model):
    TYPES = (
        (1, "Fundacja"),
        (2, "Organizacja pozarządowa"),
        (3, "Zbiórka lokalna")
    )

    def __str__(self):
        return f"{self.name} & ' ' & {self.get_type_display} "
    
    
    name = models.CharField(max_length=128,  null=False, verbose_name="Nazwa")
    description= models.TextField(verbose_name="Opis")
    type = models.IntegerField(choices=TYPES, default=0, verbose_name="Typ")
    categories = models.ManyToManyField(Category, verbose_name="Kategorie")


class Donation(models.Model):
    categories = models.ManyToManyField(Category, verbose_name="Kategorie")
    institution = models.ForeignKey(Institution, verbose_name="Instytucja", on_delete=models.CASCADE)
    address = models.CharField(max_length=128, verbose_name="Adres")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon")
    city = models.CharField(max_length=50, verbose_name="Miejscowość")
    zip_code = models.CharField(max_length=50, verbose_name="Kod pocztowy")
    pick_up_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Data odbioru")
    pick_up_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Czas odbioru")
    pick_up_comment = models.TextField(verbose_name="Komentarz do odbioru")
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, verbose_name="Użytkownik")

"""
quantity (liczba worków)
- categories (relacja ManyToMany do modelu Category)
- institution (klucz obcy do modelu Institution)
- address (ulica plus numer domu)
- phone_number (numer telefonu)
- city
- zip_code
- pick_up_date
- pick_up_time
- pick_up_comment  
 - user (klucz obcy do tabeli user; domyślna tabela zakładana przez django; może być Nullem, domyślnie Null).
 """