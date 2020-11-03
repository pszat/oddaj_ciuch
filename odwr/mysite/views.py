from django.shortcuts import render
from django import views

# Create your views here.


class LandingPage(views.View):
    def get(self, request):
        return render(request, 'mysite/index.html')


class Register(views.View):
    def get(self, request):
        return render(request, 'mysite/register.html')


class Login(views.View):
    def get(self, request):
        return render(request, 'mysite/login.html')


class AddDonation(views.View):
    def get(self, request):
        return render(request, 'mysite/add-donation.html')