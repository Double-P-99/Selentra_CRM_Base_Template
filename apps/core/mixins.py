"""Reusable view mixins for the CRM."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CRMLoginRequiredMixin(LoginRequiredMixin):
    """Mixin that redirects unauthenticated users to login."""
    pass


class SuccessMessageMixin:
    """Mixin that adds a success message on form save."""

    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class OwnedByUserMixin:
    """Filter queryset to objects belonging to the current user."""

    owner_field = 'assigned_to'

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(**{self.owner_field: self.request.user})
        return qs
