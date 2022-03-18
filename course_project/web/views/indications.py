from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views import generic as views

from course_project.web.models import Client, Taxes


class IndicationsListView(PermissionRequiredMixin, views.ListView):
    permission_required = ('web.view_client',)
    model = Client
    paginate_by = 2
    template_name = 'indications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taxes = Taxes.objects.all()[0]
        context['price'] = taxes.price
        context['tax'] = taxes.tax
        return context