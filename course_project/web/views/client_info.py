import json

from django.views import generic as views

from course_project.web.models import Client, Archive


class ClientDetailsView(views.DetailView):
    model = Client
    template_name = 'client-detals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archives = Archive.objects.all()
        labels = []
        data = []
        data_color = []
        for arch in archives:
            clients = json.loads(arch.data)
            labels.append(arch.from_date)
            cl = [c for c in clients if c['pk'] == self.object.pk][0]
            data.append(cl['fields']['new'] - cl['fields']['old'])

        middle = max(data) / 2
        labels = list(map(lambda d: d.strftime("%d-%m-%Y"), labels))
        labels.reverse()
        data.reverse()
        for d in data:
            # data_color.append(f'rgba(255,{int(255 - (255 * d / max(data)))},0,.4)')
            if d < middle:
                data_color.append(f'rgba({int(255 * d / middle)},255,0,.3)')
            else:
                data_color.append(f'rgba(255,{int(255-(255 * (d / middle - 1)))},0,.3)')

        context['labels'] = json.dumps(labels)
        context['data'] = json.dumps(data)
        context['data_color'] = json.dumps(data_color)

        print(context)
        return context
