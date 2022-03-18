import json

from django.shortcuts import render, redirect

from course_project.web.models import Archive


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
