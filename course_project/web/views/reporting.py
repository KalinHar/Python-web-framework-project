from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from course_project.web.models import Client, Taxes, OldDebts, Archive, Master


def reporting_view(request):
    if not request.user.has_perm('web.add_archive',):
        return redirect('403')

    object_list = Client.objects.all()
    taxes = Taxes.objects.first()
    master = Master.objects.first()

    context = {
        'object_list': object_list,
        'master': master,
    }
    if Client.objects.filter(reported=False).count() == 0:
        context['all_reported'] = True
    else:
        context['all_reported'] = False

    def report_master(m_units):
        if not m_units.isdecimal() or int(m_units) < master.new:
            messages.error(request, 'Incorrect units!')
            return

        master.old = master.new
        master.new = int(m_units)
        master.reported = True
        master.save()

        context['clients_kw'] = sum(cl.difference for cl in object_list)
        context['master_kw'] = master.difference
        context['report_done'] = True

    def add_client_to_olddebts(client):
        new_debt = OldDebts()
        new_debt.indications = f'{client.new} - {client.old} = {client.new - client.old}'
        new_debt.debts = client.difference * taxes.price + taxes.tax
        new_debt.client = client
        new_debt.save()
        client.old_debts += 1

    def report_client(client_id, client_units):
        client = object_list.get(pk=client_id)
        if not client_units.isdecimal() or int(client_units) < client.new:
            messages.error(request, 'Incorrect units!')
            return
        if not client.paid:
            add_client_to_olddebts(client)

        client.old = client.new
        client.new = int(client_units)
        client.reported = True
        client.paid = False
        client.save()

        if Client.objects.filter(reported=False).count() == 0:
            master.reported = False
            master.save()

    if request.method == 'GET':
        client_units = request.GET.get('units', None)
        client_id = request.GET.get('id', None)
        master_units = request.GET.get('m_units', None)
        if client_id:
            report_client(client_id, client_units)
        if master_units:
            report_master(master_units)

    return render(request, 'reporting/reporting.html', context)


class EditUnitsView(PermissionRequiredMixin, views.TemplateView):
    permission_required = ('web.add_archive',)

    def get_client(self, pk):
        client = Client.objects.filter(pk=pk).first()
        if client:
            context = self.get_context_data()
            context['client'] = client
            return context
        messages.error(self.request, 'Incorrect client number!')

    def edit_units(self, units, pk):
        client = Client.objects.get(pk=pk)
        if client.old < int(units):
            client.new = int(units)
            client.save()
            return True
        messages.error(self.request, 'Incorrect units!')

    def get(self, request, *args, **kwargs):
        client_pk = request.GET.get('client_pk', None)
        new_units = request.GET.get('new_units', None)

        if new_units:
            if self.edit_units(new_units, client_pk):
                return HttpResponseRedirect(reverse_lazy('indications'))
        if client_pk:
            context = self.get_client(client_pk)
            if context:
                return render(request, 'reporting/edit-units.html', context=context)
        return render(request, 'reporting/edit-units.html')


class EditMasterView(PermissionRequiredMixin, views.UpdateView):
    permission_required = ('web.add_archive',)
    model = Master
    fields = '__all__'
    template_name = 'reporting/edit-master.html'
    success_url = reverse_lazy('indications')

    def get_object(self, queryset=None):
        obj = self.model.objects.first()
        return obj

    def form_valid(self, form):
        old = form.data['old']
        new = form.data['new']
        if 0 < int(old) <= int(new):
            messages.success(self.request, 'Master units successful updated.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Incorrect Master units!')
            return super().form_invalid(form)


def add_archive(request):
    MAXIMUM_ARCHIVES = 12
    if not request.user.has_perm('web.add_archive',):
        return redirect('403')
    data = list(Client.objects.all())
    taxes = list(Taxes.objects.all())
    if Archive.objects.count() == MAXIMUM_ARCHIVES:
        Archive.objects.last().delete()
    new_archive = Archive()
    new_archive.data = serializers.serialize('json', data)
    new_archive.taxes = serializers.serialize('json', taxes)
    new_archive.save()

    Client.objects.all().update(reported=False)

    return redirect('reporting')
