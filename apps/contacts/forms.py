"""Forms for contacts."""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Contact, Company, Note


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'mobile',
            'job_title', 'company', 'status', 'lead_source',
            'address', 'city', 'country', 'description', 'assigned_to', 'tags',
        ]
        widgets = {'tags': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            Row(
                Column('job_title', css_class='col-md-6'),
                Column('company', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-6'),
                Column('lead_source', css_class='col-md-6'),
            ),
            Row(
                Column('city', css_class='col-md-6'),
                Column('country', css_class='col-md-6'),
            ),
            'address',
            'description',
            'assigned_to',
            'tags',
            Submit('submit', 'Save Contact', css_class='btn btn-primary mt-2'),
        )


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'industry', 'size', 'website', 'phone', 'email',
            'address', 'city', 'country', 'description', 'annual_revenue', 'assigned_to',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-8'),
                Column('industry', css_class='col-md-4'),
            ),
            Row(
                Column('website', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('size', css_class='col-md-6'),
            ),
            Row(
                Column('city', css_class='col-md-6'),
                Column('country', css_class='col-md-6'),
            ),
            'address',
            Row(
                Column('annual_revenue', css_class='col-md-6'),
                Column('assigned_to', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Company', css_class='btn btn-primary mt-2'),
        )


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'content',
            Submit('submit', 'Add Note', css_class='btn btn-secondary btn-sm'),
        )
