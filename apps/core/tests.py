"""Basic smoke tests for the CRM base template."""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthViewTests(TestCase):
    """Test authentication views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123',
            email='test@example.com', role='sales'
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign in')

    def test_login_redirects_unauthenticated_dashboard(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertRedirects(response, '/accounts/login/?next=/', fetch_redirect_response=False)

    def test_login_success(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser', 'password': 'testpass123'
        })
        self.assertRedirects(response, '/', fetch_redirect_response=False)

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, '/accounts/login/', fetch_redirect_response=False)


class DashboardViewTests(TestCase):
    """Test dashboard view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', role='sales'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_dashboard_renders(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')

    def test_dashboard_context_keys(self):
        response = self.client.get(reverse('dashboard:index'))
        ctx = response.context
        self.assertIn('total_contacts', ctx)
        self.assertIn('total_deals', ctx)
        self.assertIn('pending_activities', ctx)


class ContactViewTests(TestCase):
    """Test contact views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', role='sales'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_contact_list_renders(self):
        response = self.client.get(reverse('contacts:contact_list'))
        self.assertEqual(response.status_code, 200)

    def test_contact_create_renders(self):
        response = self.client.get(reverse('contacts:contact_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Contact')

    def test_company_list_renders(self):
        response = self.client.get(reverse('contacts:company_list'))
        self.assertEqual(response.status_code, 200)


class DealsViewTests(TestCase):
    """Test deals views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', role='sales'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_deal_list_renders(self):
        response = self.client.get(reverse('deals:deal_list'))
        self.assertEqual(response.status_code, 200)

    def test_deal_pipeline_renders(self):
        response = self.client.get(reverse('deals:deal_pipeline'))
        self.assertEqual(response.status_code, 200)


class ActivitiesViewTests(TestCase):
    """Test activities views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', role='sales'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_activity_list_renders(self):
        response = self.client.get(reverse('activities:activity_list'))
        self.assertEqual(response.status_code, 200)

    def test_activity_create_renders(self):
        response = self.client.get(reverse('activities:activity_create'))
        self.assertEqual(response.status_code, 200)


class APIViewTests(TestCase):
    """Test REST API endpoints."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', role='sales'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_api_contacts_list(self):
        response = self.client.get('/api/v1/contacts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())

    def test_api_deals_list(self):
        response = self.client.get('/api/v1/deals/')
        self.assertEqual(response.status_code, 200)

    def test_api_activities_list(self):
        response = self.client.get('/api/v1/activities/')
        self.assertEqual(response.status_code, 200)
