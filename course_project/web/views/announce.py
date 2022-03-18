import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from course_project.web.forms import AddAnnounceForm, EditAnnounceForm, DeleteAnnounceForm
from course_project.web.models import Notice


class AnnounceView(views.ListView):
    model = Notice
    template_name = 'announce/announce.html'


class AddAnnounceView(LoginRequiredMixin, views.CreateView):
    model = Notice
    form_class = AddAnnounceForm
    template_name = 'announce/add-announce.html'
    success_url = reverse_lazy('announce')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "New Notice add successful.")
        return super().form_valid(form)


class EditAnnounceView(views.UpdateView):
    model = Notice
    form_class = EditAnnounceForm
    template_name = 'announce/edit-announce.html'
    success_url = reverse_lazy('announce')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            return redirect('403')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        notice = self.get_object()
        new_img = form.cleaned_data['image']
        if notice.image and new_img != notice.image:
            os.remove(notice.image.path)
        messages.success(self.request, "Notice successful edited.")
        return super().form_valid(form)


class DeleteAnnounceView(views.DeleteView):
    template_name = 'web/confirm_delete.html'
    form_class = DeleteAnnounceForm
    model = Notice
    success_url = reverse_lazy('announce')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            return redirect('403')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance = self.object
        notice = self.get_object()
        if notice.image:
            os.remove(notice.image.path)
        messages.warning(self.request, "Delete successful.")
        return super().form_valid(form)
