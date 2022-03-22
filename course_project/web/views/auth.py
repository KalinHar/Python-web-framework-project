from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

from django.shortcuts import render, redirect
from django.views import generic as views

from course_project.web.forms import UserModel


class LoginFormView(LoginView):
    template_name = 'auth/login.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})


class RegisterFormView(views.CreateView):
    template_name = 'auth/register.html'
    form_class = UserCreationForm

    # def get(self, request):
    #     form = self.form_class()
    #     message = ''
    #     return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        username = form.data['username']
        password1 = form.data['password1']
        password2 = form.data['password2']
        users = [u.username for u in UserModel.objects.all()]

        if username in users:
            message = 'Username exist!'
        elif len(password1) < 8:
            message = 'Password must contains digit and letters, and be at least 8 symbols.'
        elif password1 != password2:
            message = "Passwords don't match."
        else:
            message = 'Unsuccessful registration!'
        return render(request, self.template_name, context={'form': form, 'message': message})
