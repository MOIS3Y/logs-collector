from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Ticket


class CreateTicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['number', 'platform', 'note']
        widgets = {
            'platform': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(CreateTicketForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.attrs = {"novalidate": ''}

        self.helper.layout = Layout(
            Div(FloatingField('number'), 'platform', css_class='col-md-2'),
            Div('note', css_class='col-md-6'),
            Submit('submit', 'Create', css_class='btn btn-success'),
        )
