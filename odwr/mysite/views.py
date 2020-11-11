from django.shortcuts import render, redirect, reverse
from django import views
from django.db.models import Sum, Count
from mysite import models
from mysite import forms
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse

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
            
            user.save()
            messages.add_message(request, messages.INFO, 'Pomyślnie dodano nowego użytkownika')
            return redirect(reverse('login'))
        else:
            return render(request, "mysite/register.html", ctx)

class Login(views.View):
    def get(self, request):
        return render(request, "mysite/login.html")

    def post(self, request):
        email = request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect(reverse('landing-page'))
        else:
            # No backend authenticated the credentials
            if models.User.objects.filter(username=email).count() == 0:
                messages.add_message(request, messages.WARNING, 'Taki użytkownik nie istnieje')
                return redirect(reverse('register'))
            else:
                messages.add_message(request, messages.WARNING, 'Złe hasło')
                return render(request, "mysite/login.html", {'email':email})                


class Logout(views.View):
    def get(self, request):
        logout(request)
        return redirect(reverse('landing-page'))


class AddDonation(views.View):
    def get(self, request):
        institutions = models.Institution.objects.all()
        categories = models.Category.objects.filter(institution__in=institutions).distinct()
        ctx = {
            'categories': categories
        }
        return render(request, "mysite/add-donation.html", ctx)
        
    def post(self, request):
        print("yeey")
        return redirect(reverse('landing-page'))


def get_institutions_by_categories(request):
    categories = request.GET.get('categories')
    print('dupa')
    # print(request.GET)
    print(categories)
    if categories is None:
        institutions = models.Institution.objects.get(id=0).values()
    else:
        institutions = models.Institution.objects.filter(categories__in=categories).distinct().values()

    institutions_list = list(institutions)
    return JsonResponse(institutions_list, safe=False)