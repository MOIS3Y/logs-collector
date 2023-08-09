from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Ticket


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['number', 'attempts', 'platform', 'note']
        widgets = {
            'platform': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.attrs = {"novalidate": ''}

        self.helper.layout = Layout(
            Div(
                FloatingField('number', 'attempts'),
                'platform',
                css_class='col-lg-2'
            ),
            Div('note', css_class='col-lg-6'),
            Submit('submit', 'Save', css_class='btn btn-primary'),
        )
