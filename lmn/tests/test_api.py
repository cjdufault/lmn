from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from django.http import HttpResponseServerError

from lmn.api_views import not_authorized_message, unavailable_message

class ApiTests(TestCase):
    
    # # 401 errors should show the not_authorized_message and respond with 500
    def test_artist_server_error(self):
        url = reverse('admin_get_artist')
        response = self.client.get(url)
        self.assertContains(response, not_authorized_message, status_code=500)
        self.assertEqual(response.status_code, 500)

    def test_venue_server_error(self):
        url = reverse('admin_get_venue')
        response = self.client.get(url)
        self.assertContains(response, not_authorized_message, status_code=500)
        self.assertEqual(response.status_code, 500)

    def test_show_server_error(self):
        url = reverse('admin_get_show')
        response = self.client.get(url)
        self.assertContains(response, not_authorized_message, status_code=500)
        self.assertEqual(response.status_code, 500)

    # all other exceptions show the unavailable_message and respond with 500
    @patch('requests.get', side_effect=[Exception])
    def test_artist_server_error_500(self, requests_mock):
        url = reverse('admin_get_artist')
        response = self.client.get(url)
        self.assertContains(response, unavailable_message, status_code=500)
        self.assertEqual(response.status_code, 500)

    @patch('requests.get', side_effect=[Exception])
    def test_venue_server_error_500(self, requests_mock):
        url = reverse('admin_get_venue')
        response = self.client.get(url)
        self.assertContains(response, unavailable_message, status_code=500)
        self.assertEqual(response.status_code, 500)

    @patch('requests.get', side_effect=[Exception])
    def test_show_server_error_500(self, requests_mock):
        url = reverse('admin_get_show')
        response = self.client.get(url)
        self.assertContains(response, unavailable_message, status_code=500)
        self.assertEqual(response.status_code, 500)
