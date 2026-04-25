"""Forms for user accounts."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import User


class CRMLoginForm(AuthenticationForm):
    """Styled login form."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Sign In', css_class='btn btn-primary w-100 mt-2'),
        )


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            'email',
            'phone',
            'bio',
            'avatar',
            Submit('submit', 'Save Changes', css_class='btn btn-primary'),
        )


class UserCreateForm(UserCreationForm):
    """Admin form for creating new users."""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'team',
                  'phone', 'password1', 'password2']
