from django.shortcuts import render
from django import views

# Create your views here.


class LandingPage(views.View):
    def get(self, request):
        return render(request, 'mysite/index.html')