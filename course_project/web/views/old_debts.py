from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import redirect
from django.views import generic as views

from course_project.web.models import Client, OldDebts


class OldDebtsView(PermissionRequiredMixin, views.ListView):
    permission_required = ('web.change_taxes',)
    model = OldDebts
    template_name = 'payments/old-debts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = 'all'
        context['pay_btn'] = True

        return context


class ClientOldDebtsView(PermissionRequiredMixin, views.ListView):
    permission_required = ('web.view_client',)
    model = OldDebts
    template_name = 'payments/old-debts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pay_btn = False
        if self.request.user.has_perm('web.change_taxes'):
            pay_btn = True
        object_list = [obj for obj in self.object_list if obj.client.pk == self.kwargs['pk']]
        context.update({
            'object_list': object_list,
            'pay_btn': pay_btn,
        })
        return context


def clear_debt(request, pk):
    if not request.user.has_perm('web.change_taxes',):
        return redirect('403')
    debt = OldDebts.objects.get(pk=pk)
    client = Client.objects.get(pk=debt.client.pk)
    client.old_debts -= 1
    client.save()
    debt.delete()
    messages.warning(request, "Payment successful.")
    return redirect('payments')
