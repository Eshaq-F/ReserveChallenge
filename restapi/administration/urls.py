from django.urls import path
from administration.views import GetReportView

app_name = 'administration'

urlpatterns = [
    path('get-report/', GetReportView.as_view(), name='get_report'),
]
