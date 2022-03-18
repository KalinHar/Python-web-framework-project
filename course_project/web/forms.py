from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from course_project.web.models import Client, Notice, Taxes

UserModel = get_user_model()


class LoginForm(forms.ModelForm):

    class Meta:
        model = UserModel
        fields = ('username', 'password',)
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username',
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'placeholder': 'Password',
                    'class': 'form-control',
                    'type': 'password',
                }
            ),
        }


class RegisterForm(UserCreationForm):

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user

    class Meta:
        model = UserModel
        fields = ("username", "password1", "password2")


class EditClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f_name, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            field.widget.attrs['class'] = 'form-floating mb-3'
            if f_name == 'username':
                field.disabled = True

    class Meta:
        model = Client
        fields = ('username', 'names', 'phone', 'paid')


class AddAnnounceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f_name, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            field.widget.attrs['placeholder'] = f_name
            field.widget.attrs['class'] = 'form-floating mb-3'

    class Meta:
        model = Notice
        fields = ('title','content', 'image',)


class EditAnnounceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f_name, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            field.widget.attrs['class'] = 'form-floating mb-3'
            if f_name == 'author':
                field.disabled = True

    class Meta:
        model = Notice
        fields = '__all__'


class DeleteAnnounceForm(forms.ModelForm):

    class Meta:
        model = Notice
        fields = ()


class UpdateTaxesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f_name, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            field.widget.attrs['class'] = 'form-floating mb-3'

    class Meta:
        model = Taxes
        fields = '__all__'
