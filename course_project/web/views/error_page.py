from django.shortcuts import render
from django.views import generic as views


class ForbiddenPageView(views.View):
    def get(self, request):
        return render(request, '403.html')