import os
from logging import getLogger

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView

from administration.forms import ReservationReportForm
from administration.utils import to_text, to_html
from reservation.models import Reserve

logger = getLogger(__name__)


class GetReportView(TemplateView):
    template_name = 'report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReservationReportForm()
        return context

    def get(self, request, *args, **kwargs):
        if auth_fail := self.check_auth():
            return auth_fail
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        if auth_fail := self.check_auth():
            return auth_fail

        form = ReservationReportForm(request.POST)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(**{'status': 'error', 'message': form.errors}))

        queryset = self.get_reservations(form)
        if form.cleaned_data['file'] == ReservationReportForm.TEXT:
            content_type, file_path = 'text/plain', to_text(queryset)
        else:
            content_type, file_path = 'text/html', to_html(queryset)
        with open(file_path, 'r') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response

    def check_auth(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse('admin:login') + f'?next={self.request.path}')

    @staticmethod
    def get_reservations(form: ReservationReportForm) -> QuerySet:
        start, end = form.cleaned_data['from_dt'], form.cleaned_data['end_dt']
        return Reserve.objects.filter(from_dt__lte=end, to_dt__gte=start)
