"""Views for contacts and companies."""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from apps.core.mixins import CRMLoginRequiredMixin, SuccessMessageMixin
from .models import Contact, Company, Note
from .forms import ContactForm, CompanyForm, NoteForm


# ── Contacts ──────────────────────────────────────────────────────────────────

class ContactListView(CRMLoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 20

    def get_queryset(self):
        qs = Contact.objects.select_related('company', 'assigned_to').filter(is_active=True)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) |
                Q(email__icontains=q) | Q(company__name__icontains=q)
            )
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = Contact.STATUS_CHOICES
        ctx['q'] = self.request.GET.get('q', '')
        ctx['status_filter'] = self.request.GET.get('status', '')
        return ctx


class ContactDetailView(CRMLoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['note_form'] = NoteForm()
        ctx['notes'] = self.object.notes.select_related('author').all()
        ctx['deals'] = self.object.deals.select_related('assigned_to').all()
        ctx['activities'] = self.object.activities.select_related('assigned_to').all()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.contact = self.object
            note.author = request.user
            note.save()
            messages.success(request, 'Note added.')
        return self.get(request, *args, **kwargs)


class ContactCreateView(CRMLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_message = 'Contact created successfully.'

    def form_valid(self, form):
        if not form.instance.assigned_to:
            form.instance.assigned_to = self.request.user
        return super().form_valid(form)


class ContactUpdateView(CRMLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_message = 'Contact updated successfully.'


class ContactDeleteView(CRMLoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contacts:contact_list')

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        messages.success(self.request, 'Contact deleted.')
        return self._redirect_to_success_url()

    def _redirect_to_success_url(self):
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.success_url)


# ── Companies ─────────────────────────────────────────────────────────────────

class CompanyListView(CRMLoginRequiredMixin, ListView):
    model = Company
    template_name = 'contacts/company_list.html'
    context_object_name = 'companies'
    paginate_by = 20

    def get_queryset(self):
        qs = Company.objects.filter(is_active=True)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class CompanyDetailView(CRMLoginRequiredMixin, DetailView):
    model = Company
    template_name = 'contacts/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['note_form'] = NoteForm()
        ctx['notes'] = self.object.notes.select_related('author').all()
        ctx['contacts'] = self.object.contacts.filter(is_active=True)
        ctx['deals'] = self.object.deals.select_related('assigned_to').all()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.company = self.object
            note.author = request.user
            note.save()
            messages.success(request, 'Note added.')
        return self.get(request, *args, **kwargs)


class CompanyCreateView(CRMLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'contacts/company_form.html'
    success_message = 'Company created successfully.'


class CompanyUpdateView(CRMLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'contacts/company_form.html'
    success_message = 'Company updated successfully.'
