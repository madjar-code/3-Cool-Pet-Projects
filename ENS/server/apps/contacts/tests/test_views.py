import uuid
from rest_framework import status
from rest_framework.test import APITestCase
from contacts.models import (
    PriorityChoices,
    Contact,
)
from server.urls import API_PREFIX


class TestContactViews(APITestCase):
    def setUp(self) -> None:
        self.contact1: Contact = Contact.objects.create(
            name='test1',
            email='test1@test.com',
            phone='+12125552362',
            priority_group=\
                PriorityChoices.LOW_PRIORITY,
        )
        self.contact2: Contact = Contact.objects.create(
            name='test2',
            email='test2@test.com',
            phone='+12125552362',
            priority_group=\
                PriorityChoices.HIGH_PRIORITY,
        )
        self.correct_contact_data = {
            'name': 'John',
            'email': 'john@example.com',
            'phone': '+12125552368',
            'priority_group': 'Low'
        }
        self.incorrect_contact_data = {
            'name': 'John',
            'priority_group': 'Low'
        }
        self.contact_data1 = {
            'name': 'John',
            'email': 'john@example.com',
            'phone': '+12125552368',
            'priority_group': PriorityChoices.LOW_PRIORITY,
        }
        self.contact_data2 = {
            'name': 'Jane',
            'email': 'jane@example.com',
            'phone': '+12125552369',
            'priority_group': PriorityChoices.HIGH_PRIORITY,
        }
        self.contact_data3 = {
            'name': 'Alice',
            'email': 'alice@example.com',
            'phone': '+12125552370',
            'priority_group': PriorityChoices.LOW_PRIORITY,
        }

    def test_get_contacts_list(self) -> None:
        response = self.client.get(f'/{API_PREFIX}/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_contact_details(self) -> None:
        url = f'/{API_PREFIX}/contacts/{self.contact1.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notifications']['success'], 0)
        self.assertEqual(response.data['notifications']['failed'], 0)

    def test_get_non_existent_contact_details(self) -> None:
        invalid_uuid = str(uuid.uuid4())
        url = f'/{API_PREFIX}/contacts/{invalid_uuid}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Contact with `id` not found')

    def test_create_contact(self) -> None:
        response = self.client.post(f'/{API_PREFIX}/contacts/create/',
                                   self.correct_contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_contact_invalid(self) -> None:
        response = self.client.post(f'/{API_PREFIX}/contacts/create/',
                                   self.incorrect_contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_multiple_contacts(self):
        contacts_data = [self.contact_data1, self.contact_data2, self.contact_data3]
        response = self.client.post(f'/{API_PREFIX}/contacts/create-multiply/', data=contacts_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['contacts']), len(contacts_data))

    def test_create_multiple_contacts_with_duplicate_emails(self):
        contacts_data = [self.contact_data1, self.contact_data2, self.contact_data1]
        response = self.client.post(f'/{API_PREFIX}/contacts/create-multiply/', data=contacts_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['errors']), 1)

    def test_create_multiple_contacts_with_invalid_data(self) -> None:
        contacts_data = [
            {
                'name': 'John',
                # 'email': 'john@example.com',
                # 'phone': '+12125552368',
                'priority_group': PriorityChoices.LOW_PRIORITY,
            },
            {
                'name': 'Jane',
                'email': 'jane@example.com',
                'phone': '+12125552369',
                'priority_group': PriorityChoices.HIGH_PRIORITY,
            },
        ]
        response = self.client.post(f'/{API_PREFIX}/contacts/create-multiply/', data=contacts_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['errors']), 1)

    def test_delete_existing_contact(self) -> None:
        response = self.client.delete(f'/{API_PREFIX}/contacts/delete/{self.contact1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.active_objects.filter(id=self.contact1.id).exists())

    def test_delete_non_existent_contact(self) -> None:
        invalid_uuid = str(uuid.uuid4())
        url = f'/{API_PREFIX}/contacts/delete/{invalid_uuid}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Contact with `id` not found')

    def test_update_existing_contact(self) -> None:
        data = {
            'name': 'Updated John',
            'email': 'updated_john@example.com',
            'phone': '+12125552369',
            'priority_group': PriorityChoices.HIGH_PRIORITY,
        }
        response = self.client.put(f'/{API_PREFIX}/contacts/update/{self.contact2.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact2.refresh_from_db()
        self.assertEqual(self.contact2.name, 'Updated John')
        self.assertEqual(self.contact2.email, 'updated_john@example.com')
        self.assertEqual(self.contact2.phone, '+12125552369')
        self.assertEqual(self.contact2.priority_group, PriorityChoices.HIGH_PRIORITY)

    def test_update_non_existent_contact(self) -> None:
        invalid_uuid = str(uuid.uuid4())
        data = {
            'name': 'Updated John',
            'email': 'updated_john@example.com',
            'phone': '+12125552369',
            'priority_group': PriorityChoices.HIGH_PRIORITY,
        }
        response = self.client.put(f'/{API_PREFIX}/contacts/update/{invalid_uuid}/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Contact with `id` not found')
