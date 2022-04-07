import csv
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from course_project.web.models import Archive


def view_archive(request, pk):
    if not request.user.has_perm('web.view_client',):
        return redirect('403')
    archive_list = Archive.objects.all()
    arch = next(x for x in archive_list if x.pk == pk)
    from_date = arch.from_date
    clients = json.loads(arch.data)
    taxes = json.loads(arch.taxes)

    context = {
        'all': archive_list,
        'only_one': True,
        'from_date': from_date,
        'clients': clients,
        'taxes': taxes[0],
        'arch_pk': arch.pk,
    }
    return render(request, 'archive.html', context)


def all_archive(request):
    if not request.user.has_perm('web.view_client',):
        return redirect('403')
    archive_list = Archive.objects.all()
    context = {
        'all': archive_list,
        'only_one': False,
    }
    return render(request, 'archive.html', context)


def download_archive(request, pk):
    arch = Archive.objects.get(pk=pk)
    from_date = arch.from_date
    clients = json.loads(arch.data)
    taxes = json.loads(arch.taxes)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export-archive.csv"'
    writer = csv.writer(response)
    writer.writerow([f'date: {from_date.date()}, price: {taxes[0]["fields"]["price"]}, tax: {taxes[0]["fields"]["tax"]}'])
    writer.writerow(['id', 'names', 'old', 'new'])
    for cl in clients:
        writer.writerow([cl['pk'], cl['fields']['names'], cl['fields']['old'], cl['fields']['new']])
    return response
