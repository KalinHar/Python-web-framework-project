from django.shortcuts import render
from django.views import generic as views


class HomeView(views.View):
    def get(self, request):
        return render(request, 'home.html')

