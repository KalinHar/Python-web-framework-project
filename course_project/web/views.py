import json
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from course_project.web.forms import LoginForm, RegisterForm, EditClientForm, AddAnnounceForm, UserModel, \
    EditAnnounceForm, DeleteAnnounceForm, UpdateTaxesForm
from course_project.web.models import Client, Taxes, Notice, OldDebts, Archive, Master

# Todo: Perms and auth, modal for delete announce, homePage, expand img in announce ...


class HomeView(views.View):
    def get(self, request):
        return render(request, 'home.html')


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
        if len(username) < 4:
            message = 'Too short username, , must be at least 4 symbols!'
        elif username in users:
            message = 'Username exist!'
        elif len(password1) < 8:
            message = 'Password must contains digit and letters, and be at least 8 symbols.'
        elif password1 != password2:
            message = "Passwords don't match."
        else:
            message = 'Unsuccessful registration!'
        return render(request, self.template_name, context={'form': form, 'message': message})


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


class AnnounceView(views.ListView):
    model = Notice
    template_name = 'announce.html'


class AddAnnounceView(LoginRequiredMixin, views.CreateView):
    model = Notice
    form_class = AddAnnounceForm
    # fields = ('title', 'content', 'image',)
    template_name = 'addannounce.html'
    success_url = reverse_lazy('announce')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "New Notice add successful.")
        return super().form_valid(form)

    # def get_initial(self):
    #     return {
    #         'author': self.request.user,
    #     }


class EditAnnounceView(views.UpdateView):
    model = Notice
    form_class = EditAnnounceForm
    # fields = ('title', 'content', 'image',)
    template_name = 'editannounce.html'
    success_url = reverse_lazy('announce')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            return redirect('403')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # form.instance.author = self.request.user
        notice = self.get_object()
        new_img = form.cleaned_data['image']
        if notice.image and new_img != notice.image:
            os.remove(notice.image.path)
        messages.success(self.request, "Notice successful edited.")
        return super().form_valid(form)


class DeleteAnnounce(views.DeleteView):
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



def delete_announce(request, pk):
    notice = Notice.objects.get(pk=pk)
    if request.user != notice.author:
        return redirect('403')
    if notice.image:
        notice_path = notice.image.path
        os.remove(notice_path)
    notice.delete()
    messages.warning(request, "Delete successful.")
    return redirect('announce')


class OldDebtsView(PermissionRequiredMixin, views.ListView):
    permission_required = ('web.change_taxes',)
    model = OldDebts
    template_name = 'olddebts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = 'all'
        context['pay_btn'] = True

        return context


class ClientOldDebtsView(PermissionRequiredMixin, views.ListView):
    permission_required = ('web.view_client',)
    CASHER = 'nushka'
    model = OldDebts
    template_name = 'olddebts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        casher = UserModel.objects.get(username=self.CASHER)
        pay_btn = False
        if self.request.user == casher:
            pay_btn = True
        object_list = [obj for obj in self.object_list if obj.client.pk == self.kwargs['pk']]
        context.update({
            'object_list': object_list,
            'pay_btn': pay_btn,
        })
        return context


def client_debts(request, pk):
    casher = UserModel.objects.get(username='nushka')
    pay_btn = False
    if request.user == casher:
        pay_btn = True
    object_list = OldDebts.objects.filter(client_id=pk).all()
    context = {
        'object_list': object_list,
        'pay_btn': pay_btn,
    }
    return render(request, 'olddebts.html', context)


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


class PaymentsView(PermissionRequiredMixin, views.ListView):
    permission_required = ('web.change_taxes',)
    model = Client
    template_name = 'payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        taxes = Taxes.objects.all()[0]
        master = Master.objects.all()[0]
        clients = self.object_list
        debit = sum(map(lambda cl_p: cl_p.difference * taxes.price + taxes.tax, filter(lambda cl: cl.paid, clients)))
        total = sum(map(lambda cl: cl.difference * taxes.price + taxes.tax, clients))

        context['m_units'] = master.difference
        context['m_cost'] = master.difference * taxes.price
        context['price'] = taxes.price
        context['tax'] = taxes.tax
        context['debit'] = debit
        context['total'] = total

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
    # fields = '__all__'
    template_name = 'taxes.html'
    success_url = reverse_lazy('indications')

    def get_context_data(self, **kwargs):
        paid_clients = Client.objects.filter(paid=True).count()
        context = super().get_context_data(**kwargs)
        context['pk'] = self.TAXES_PK
        context['paid_clients'] = paid_clients
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         return super().post(self, request, *args, **kwargs)
    #     # price = form.data['price']
    #     # tax = form.data['tax']
    #     # message = ''
    #     # if float(price) < 0 or float(tax) < 0:
    #     #     message = 'The price and tax must be positive numbers!'
    #     return render(request, self.template_name, context={'form': form, 'message': message, 'pk': self.TAXES_PK})


class EditClientView(PermissionRequiredMixin, views.UpdateView):
    permission_required = ('web.change_taxes',)
    model = Client
    form_class = EditClientForm
    success_url = reverse_lazy('payments')
    template_name = 'editclient.html'

    def form_valid(self, form):
        form.instance.old_debts = self.object.old_debts
        form.instance.reported = self.object.reported
        form.instance.old = self.object.old
        form.instance.new = self.object.new

        messages.success(self.request, "Client successful edited.")
        return super().form_valid(form)


def reporting_view(request):
    if not request.user.has_perm('web.add_archive',):
        return redirect('403')
    object_list = Client.objects.all()
    taxes = Taxes.objects.all()[0]
    master = Master.objects.all()[0]

    context = {
        'object_list': object_list,
        'master': master,
    }
    if Client.objects.filter(reported=False).count() == 0:
        context['all_reported'] = True
    else:
        context['all_reported'] = False

    def report_master(m_units):
        master = Master.objects.all()[0]
        if not m_units.isdecimal() or int(m_units) < master.new:
            messages.error(request, 'Incorrect units!')
            return

        master.old = master.new
        master.new = m_units
        master.reported = True
        master.save()

        clients_kw = sum(cl.difference for cl in Client.objects.all())
        master_kw = Master.objects.all()[0].difference
        context['clients_kw'] = clients_kw
        context['master_kw'] = master_kw
        context['report_master'] = 'done'

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
        client.new = client_units
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

    return render(request, 'reporting.html', context)


class EditUnitsView(PermissionRequiredMixin, views.TemplateView):
    permission_required = ('web.add_archive',)
    def get_client(self, pk):
        client = Client.objects.filter(pk=pk).first()
        if client:
            context = self.get_context_data()
            context['client'] = client
            context['client_pk'] = client.pk
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
                return render(request, 'editunits.html', context=context)
        return render(request, 'editunits.html')


class EditMasterView(PermissionRequiredMixin, views.UpdateView):
    permission_required = ('web.add_archive',)
    model = Master
    fields = '__all__'
    template_name = 'master.html'
    success_url = reverse_lazy('indications')

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
    if not request.user.has_perm('web.add_archive',):
        return redirect('403')
    data = list(Client.objects.all())
    taxes = list(Taxes.objects.all())
    new_archive = Archive()
    new_archive.data = serializers.serialize('json', data)
    new_archive.taxes = serializers.serialize('json', taxes)
    new_archive.save()

    Client.objects.all().update(reported=False)

    return redirect('reporting')


def view_archive(request, pk):
    if not request.user.has_perm('web.view_client',):
        return redirect('403')
    all = Archive.objects.all()
    arch = next(x for x in all if x.pk == pk)
    from_date = arch.from_date
    client_data = arch.data
    tax_data = arch.taxes
    clients = json.loads(client_data)
    taxes = json.loads(tax_data)

    context = {
        'all': all,
        'only_one': True,
        'from_date': from_date,
        'clients': clients,
        'taxes': taxes[0],
    }
    return render(request, 'archive.html', context)


def all_archive(request):
    if not request.user.has_perm('web.view_client',):
        return redirect('403')
    all = Archive.objects.all()
    context = {
        'all': all,
        'only_one': False,
    }
    return render(request, 'archive.html', context)


class ForbiddenPageView(views.View):
    def get(self, request):
        return render(request, '403.html')


def announce_confirm(request):
    return render(request, 'web/notice_confirm_delete.html')