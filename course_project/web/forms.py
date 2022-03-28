from django import forms
from django.contrib.auth import get_user_model

from course_project.web.models import Client, Notice, Taxes

UserModel = get_user_model()


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
        fields = ('title', 'content', 'image',)


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
