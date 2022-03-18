from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from course_project.web.forms import EditClientForm, UpdateTaxesForm
from course_project.web.models import Client, Taxes, Master


class PaymentsView(PermissionRequiredMixin, views.ListView):
    permission_required = ('web.change_taxes',)
    model = Client
    template_name = 'payments/payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        taxes = Taxes.objects.all()[0]
        master = Master.objects.all()[0]
        clients = self.object_list
        debit = sum(map(lambda cl_p: cl_p.difference * taxes.price + taxes.tax, filter(lambda cl: cl.paid, clients)))
        total = sum(map(lambda cl: cl.difference * taxes.price + taxes.tax, clients))
        cl_units = sum(map(lambda cl: cl.difference, clients))

        context['m_units'] = master.difference
        context['m_cost'] = master.difference * taxes.price
        context['price'] = taxes.price
        context['tax'] = taxes.tax
        context['debit'] = debit
        context['total'] = total
        context['cl_units'] = cl_units

        return context


def pay_to(request, pk):
    if not request.user.has_perm('web.change_taxes',):
        return redirect('403')
    client = Client.objects.get(pk=pk)
    client.paid = True
    client.save()
    messages.warning(request, "Payment successful.")
    return redirect('payments')


class EditTaxesView(PermissionRequiredMixin, views.UpdateView):
    TAXES_PK = 1
    permission_required = ('web.change_taxes',)
    model = Taxes
    form_class = UpdateTaxesForm
    template_name = 'payments/taxes.html'
    success_url = reverse_lazy('payments')

    def get_context_data(self, **kwargs):
        paid_clients = Client.objects.filter(paid=True).count()
        context = super().get_context_data(**kwargs)
        context['pk'] = self.TAXES_PK
        context['paid_clients'] = paid_clients
        return context


class EditClientView(PermissionRequiredMixin, views.UpdateView):
    permission_required = ('web.change_taxes',)
    model = Client
    form_class = EditClientForm
    success_url = reverse_lazy('payments')
    template_name = 'payments/edit-client.html'

    def form_valid(self, form):
        form.instance.old_debts = self.object.old_debts
        form.instance.reported = self.object.reported
        form.instance.old = self.object.old
        form.instance.new = self.object.new

        messages.success(self.request, "Client successful edited.")
        return super().form_valid(form)
