from django import forms
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from crispy_forms.bootstrap import PrependedText

from .models import User


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                PrependedText(
                    'email',
                    mark_safe('<i class="bi bi-envelope-at"></i>'),
                    placeholder="email"
                ),
                PrependedText('first_name', 'First name:'),
                PrependedText('last_name', 'Last name:'),
            ),
            Submit('submit', 'Save', css_class='btn btn-primary'),
        )
