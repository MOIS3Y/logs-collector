from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Ticket, Archive


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


class ArchiveForm(forms.ModelForm):
    token = forms.UUIDField(required=True)

    class Meta:
        model = Archive
        fields = ['token', 'file']

    def __init__(self, *args, **kwargs):
        super(ArchiveForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'upload_form'

        self.helper.layout = Layout(
            Div(
                FloatingField('token'),
                'file',
                css_class='col-lg-6'
            ),
            Submit('submit', 'Upload', css_class='btn btn-primary'),
        )
