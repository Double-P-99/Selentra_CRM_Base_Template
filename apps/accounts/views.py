"""Views for user accounts."""

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.urls import reverse_lazy, is_valid_path
from django.contrib import messages
from apps.core.mixins import CRMLoginRequiredMixin
from .forms import CRMLoginForm, UserProfileForm
from .models import User


def _safe_next_url(request):
    """Return the ?next= URL only if it is a safe internal path."""
    next_url = request.GET.get('next', '')
    if next_url and is_valid_path(next_url) and next_url.startswith('/'):
        return next_url
    return reverse_lazy('dashboard:index')


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    form = CRMLoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(_safe_next_url(request))
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


class ProfileView(CRMLoginRequiredMixin, UpdateView):
    """User profile editing view."""

    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)
