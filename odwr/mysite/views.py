from django.shortcuts import render
from django import views
from django.db.models import Sum, Count
from mysite import models
from django.core.paginator import Paginator
# Create your views here.


class LandingPage(views.View):
    def get(self, request):
        donated_bags =  models.Donation.objects.all().aggregate(total=Sum('quantity'))
        supported_institutions =  models.Donation.objects.values('institution').distinct().count()
        paginator_1 = Paginator(models.Institution.objects.filter(type=1), 3)
        print(request.GET.get('page1'))
        institutions_1 = paginator_1.get_page(request.GET.get('page1'))

        paginator_2 = Paginator(models.Institution.objects.filter(type=2), 3)
        institutions_2 = paginator_2.get_page(request.GET.get('page2'))
        print(request.GET.get('page2'))

        ctx = {
            'donated_bags': donated_bags,
            'supported_institutions': supported_institutions,
            'institutions_1': institutions_1,
            'institutions_2': institutions_2
        }
        return render(request, 'mysite/index.html', ctx)



class Register(views.View):
    def get(self, request):
        return render(request, 'mysite/register.html')


class Login(views.View):
    def get(self, request):
        return render(request, 'mysite/login.html')


class AddDonation(views.View):
    def get(self, request):
        return render(request, 'mysite/add-donation.html')