import json

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
