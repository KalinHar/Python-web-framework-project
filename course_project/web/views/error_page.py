from django.shortcuts import render
from django.views import generic as views


class ForbiddenPageView(views.View):
    def get(self, request):
        return render(request, 'error-pages/403.html')


class NotExistPageView(views.View):
    def get(self, request):
        return render(request, 'error-pages/404.html')


class ServerErrorPageView(views.View):
    def get(self, request):
        return render(request, 'error-pages/500.html')