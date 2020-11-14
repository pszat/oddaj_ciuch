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
        cat = self.categories.all()
        return f'Nazwa: {self.name}, typ: {self.get_institutionType_display()}, kategorie:" {(", ").join([c.name for c in cat])}'

        
    
    
    name = models.CharField(max_length=128,  null=False, verbose_name="Nazwa")
    description= models.TextField(verbose_name="Opis", null=True, blank=True)
    institutionType = models.IntegerField(choices=TYPES, default=0, verbose_name="Typ")
    categories = models.ManyToManyField(Category, verbose_name="Kategorie")


class Donation(models.Model):
    quantity = models.IntegerField(default=0, null=False, verbose_name="Liczba worków")
    categories = models.ManyToManyField(Category, verbose_name="Kategorie")
    institution = models.ForeignKey(Institution, verbose_name="Instytucja", on_delete=models.CASCADE)
    address = models.CharField(max_length=128, verbose_name="Adres", null=True)
    phone_number = models.CharField(max_length=20, verbose_name="Telefon", null=True)
    city = models.CharField(max_length=50, verbose_name="Miejscowość", null=True)
    zip_code = models.CharField(max_length=50, verbose_name="Kod pocztowy", null=True)
    pick_up_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Data odbioru", null=True)
    pick_up_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Czas odbioru", null=True)
    pick_up_comment = models.TextField(verbose_name="Komentarz do odbioru", null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="Użytkownik")
