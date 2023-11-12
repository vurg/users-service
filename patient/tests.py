from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from .models import Patient


class PatientTestCase(TestCase):
    def setUp(self):
        Patient.objects.create(
            name="Test Patient", email="test@example.com", password="test123"
        )

    def test_get_all_patient(self):
        client = Client()
        response = client.get("/patient/")
        self.assertEqual(response.status_code, 200)

    def test_post_patient(self):
        client = Client()
        response = client.post(
            "/patient/post",
            {
                "name": "Test Patient 2",
                "email": "test2@example.com",
                "password": "test123",
            },
        )
        self.assertEqual(response.status_code, 201)
