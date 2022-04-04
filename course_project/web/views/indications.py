from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views import generic as views

from course_project.web.models import Client, Taxes


class IndicationsListView(PermissionRequiredMixin, views.ListView):
    ROWS_PER_PAGE = 5
    permission_required = ('web.view_client',)
    model = Client
    paginate_by = ROWS_PER_PAGE
    template_name = 'indications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taxes = Taxes.objects.first()
        context['price'] = taxes.price
        context['tax'] = taxes.tax
        return context
