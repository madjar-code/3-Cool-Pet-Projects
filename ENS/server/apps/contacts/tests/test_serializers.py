from typing import List
from django.test import TestCase
from contacts.api.serializers import (
    SimpleContactSerializer,
    ContactSerializer,
    CreateContactSerializer,
    UpdateContactSerializer,
)
from contacts.models import (
    PriorityChoices,
    Contact,
)


class TestContactSerializers(TestCase):
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
        
        self.correct_create_data = {
            'phone_email' : {
                'name': 'John',
                'email': 'john@example.com',
                'phone': '+12125552368',
                'priority_group': 'Low'
            },
            'email': {
                'name': 'John',
                'email': 'john@example.com',
                'priority_group': 'Low'
            },
            'phone' : {
                'name': 'John',
                'phone': '+12125552368',
                'priority_group': 'Low'
            },
        }
        
        self.wrong_create_data = {
            'no_phone_and_email': {
                'name': 'John',
                'priority_group': 'Low'
            },
            'empty_name' : {
                'name': '',
                'email': 'john@example.com',
                'priority_group': 'Low'
            },
            'incorrect_priority': {
                'name': 'John',
                'email': 'john@example.com',
                'priority_group': '12345'
            },
        }
        
        self.correct_update_data = [
            # name
            {
                'name': 'Jenna'
            },
            # phone
            {
                'phone': '+12125552368'
            },
            # email
            {
                'email': 'new@new.com'
            },
            # priority
            {
                'priority_group': 'High'
            },
            # phone and email
            {
                'phone': '+12125552368',
                'email': 'new@new.com',
            },
            # all fields
            {
                'name': 'Jenna',
                'phone': '+12125552368',
                'email': 'new@new.com',
                'priority_group': 'High',
            }
        ]

    def test_simple_serializer(self) -> None:
        contact_list = [self.contact1, self.contact2]
        serializer_data = SimpleContactSerializer(contact_list, many=True).data
        self.assertEqual(len(serializer_data), 2)
        self.assertIsInstance(serializer_data, List)
        self.assertEqual(len(serializer_data[0].keys()), 3)

    def test_details_serializer(self) -> None:
        serializer = ContactSerializer(self.contact1)
        self.assertCountEqual(
            serializer.data.keys(),
            ['id', 'name', 'email',
             'phone', 'priority_group',
             'created_at', 'is_active'])

    def test_create_serializer_email_phone(self) -> None:
        email_phone_contact = self.correct_create_data['phone_email']
        serializer = CreateContactSerializer(data=email_phone_contact)
        self.assertTrue(serializer.is_valid())

    def test_create_serializer_email(self) -> None:
        email_contact = self.correct_create_data['email']
        serializer = CreateContactSerializer(data=email_contact)
        self.assertTrue(serializer.is_valid())

    def test_create_serializer_phone(self) -> None:
        phone_contact = self.correct_create_data['phone']
        serializer = CreateContactSerializer(data=phone_contact)
        self.assertTrue(serializer.is_valid())

    def test_create_serializer_no_email_and_phone(self) -> None:
        no_email_and_phone_contact = self.wrong_create_data['no_phone_and_email']
        serializer = CreateContactSerializer(
            data=no_email_and_phone_contact)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(list(serializer.errors.keys()), ['non_field_errors'])

    def test_create_serializer_no_name(self) -> None:
        short_name_contact = self.wrong_create_data['empty_name']
        serializer = CreateContactSerializer(
            data=short_name_contact)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(list(serializer.errors.keys()), ['name'])

    def test_create_serializer_wrong_priority(self) -> None:
        incorrect_priority_contact = self.wrong_create_data['incorrect_priority']
        serializer = CreateContactSerializer(data=incorrect_priority_contact)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(list(serializer.errors.keys()), ['priority_group'])

    def test_update_serializer_name(self) -> None:
        phone_data = self.correct_update_data[0]
        serializer = UpdateContactSerializer(instance=self.contact1, data=phone_data)
        self.assertTrue(serializer.is_valid())
        updated_contact: Contact = serializer.save()
        self.assertEqual(str(updated_contact.name), 'Jenna')

    def test_update_serializer_phone(self) -> None:
        phone_data = self.correct_update_data[1]
        serializer = UpdateContactSerializer(instance=self.contact1, data=phone_data)
        self.assertTrue(serializer.is_valid())
        updated_contact: Contact = serializer.save()
        self.assertEqual(str(updated_contact.phone), '+12125552368')
