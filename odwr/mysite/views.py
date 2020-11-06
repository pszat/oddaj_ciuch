from django.shortcuts import render, redirect, reverse
from django import views
from django.db.models import Sum, Count
from mysite import models
from mysite import forms
from django.core.paginator import Paginator
from django.contrib.auth.models import User

# Create your views here.


class LandingPage(views.View):
    def get(self, request):
        donated_bags = models.Donation.objects.all().aggregate(total=Sum("quantity"))
        supported_institutions = (
            models.Donation.objects.values("institution").distinct().count()
        )
        paginator_1 = Paginator(models.Institution.objects.filter(type=1), 5)
        institutions_1 = paginator_1.get_page(request.GET.get("page1"))

        paginator_2 = Paginator(models.Institution.objects.filter(type=2), 5)
        institutions_2 = paginator_2.get_page(request.GET.get("page2"))

        paginator_3 = Paginator(models.Institution.objects.filter(type=3), 5)
        institutions_3 = paginator_3.get_page(request.GET.get("page2"))

        ctx = {
            "donated_bags": donated_bags,
            "supported_institutions": supported_institutions,
            "institutions_1": institutions_1,
            "institutions_2": institutions_2,
            "institutions_3": institutions_3,
        }
        return render(request, "mysite/index.html", ctx)


class Register(views.View):
    def get(self, request):
        form = forms.RegistrationForm()
        ctx = {"form": form}
        return render(request, "mysite/register.html", ctx)

    def post(self, request):
        form = forms.RegistrationForm(request.POST)
        ctx = {"form": form}
        if form.is_valid():
            user = models.User()
            user.username = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.set_password(form.cleaned_data.get('password'))
            return redirect(revers('login'))


class Login(views.View):
    def get(self, request):
        return render(request, "mysite/login.html")


class AddDonation(views.View):
    def get(self, request):
        return render(request, "mysite/add-donation.html")
