"""Forms for deals."""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Deal, Stage


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = [
            'title', 'pipeline', 'stage', 'contact', 'company',
            'value', 'currency', 'probability', 'expected_close_date',
            'description', 'assigned_to',
        ]
        widgets = {
            'expected_close_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Row(
                Column('pipeline', css_class='col-md-6'),
                Column('stage', css_class='col-md-6'),
            ),
            Row(
                Column('contact', css_class='col-md-6'),
                Column('company', css_class='col-md-6'),
            ),
            Row(
                Column('value', css_class='col-md-4'),
                Column('currency', css_class='col-md-4'),
                Column('probability', css_class='col-md-4'),
            ),
            Row(
                Column('expected_close_date', css_class='col-md-6'),
                Column('assigned_to', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Deal', css_class='btn btn-primary mt-2'),
        )
