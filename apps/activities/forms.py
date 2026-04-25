"""Forms for activities."""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'type', 'title', 'description', 'status', 'priority',
            'due_date', 'contact', 'company', 'deal', 'assigned_to',
        ]
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('type', css_class='col-md-4'),
                Column('status', css_class='col-md-4'),
                Column('priority', css_class='col-md-4'),
            ),
            'title',
            'description',
            Row(
                Column('due_date', css_class='col-md-6'),
                Column('assigned_to', css_class='col-md-6'),
            ),
            Row(
                Column('contact', css_class='col-md-4'),
                Column('company', css_class='col-md-4'),
                Column('deal', css_class='col-md-4'),
            ),
            Submit('submit', 'Save Activity', css_class='btn btn-primary mt-2'),
        )
