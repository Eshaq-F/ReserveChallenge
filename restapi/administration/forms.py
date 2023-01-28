from django import forms


class DateInput(forms.DateInput):
    input_type = 'datetime-local'


class ReservationReportForm(forms.Form):
    HTML = 'html'
    TEXT = 'text'
    CHOISES = [
        (HTML, 'HTML'),
        (TEXT, 'TEXT'),
    ]
    file = forms.ChoiceField(choices=CHOISES, required=True, initial=TEXT, label='file type')
    from_dt = forms.DateTimeField(required=True, label='from datetime', widget=DateInput)
    end_dt = forms.DateTimeField(required=True, label='to datetime', widget=DateInput)
