import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic as views

from course_project.web.models import Client, Archive, Notice


class ClientDetailsView(PermissionRequiredMixin, views.DetailView):
    permission_required = ('web.view_client',)
    model = Client
    template_name = 'indications-info/client-details.html'

    def get_archive_data(self):
        labels = []
        data = []
        data_color = []
        for arch in Archive.objects.all():
            clients = json.loads(arch.data)
            cl = next((c for c in clients if c['pk'] == self.object.pk), None)
            if cl:
                labels.append(arch.from_date)
                data.append(cl['fields']['new'] - cl['fields']['old'])
        if labels:
            middle = max(data) / 2
            labels = list(map(lambda label: label.strftime("%d-%m-%Y"), labels))
            labels.reverse()
            data.reverse()
            for d in data:
                # data_color.append(f'rgba(255,{int(255 - (255 * d / max(data)))},0,.4)')
                if d < middle:
                    data_color.append(f'rgba({int(255 * d / middle)},255,0,.3)')
                else:
                    data_color.append(f'rgba(255,{int(255-(255 * (d / middle - 1)))},0,.3)')

            return [labels, data, data_color]
        return [0, 0, 0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        announce_count = Notice.objects.filter(author=self.object.username).count()
        [labels, data, data_color] = self.get_archive_data()

        context['announce_count'] = announce_count
        context['labels'] = json.dumps(labels)
        context['data'] = json.dumps(data)
        context['data_color'] = json.dumps(data_color)

        return context
