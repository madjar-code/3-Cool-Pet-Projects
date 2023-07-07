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
        
        self.correct_update_data = {
            'only_name': {
                'name': 'Jenna'
            },
            'only_phone': {
                'phone': '+12125552368'
            },
            'only_email': {
                'email': 'new@new.com'
            },
            'only_priority_group': {
                'priority_group': 'High'
            },
            'email_and_phone': {
                'phone': '+12125552368',
                'email': 'new@new.com',
            },
            'all_fields': {
                'name': 'Jenna',
                'phone': '+12125552368',
                'email': 'new@new.com',
                'priority_group': 'High',
            }
        }
        
        self.wrong_update_data = {
            'empty_name': {
                'name': ''
            },
            'incorrect_phone': {
                'phone': '+1212555236'
            },
            'incorrect_email': {
                'email': 'newnew.com'
            },
            'no_phone_and_email': {
                'email': '',
                'phone': '',
            },
            'no_phone_with_no_email_instance': {
                'phone': '',
            },
            'no_email_with_no_phone_instance': {
                'email': '',
            },
        }

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
        name_data = self.correct_update_data['only_name']
        serializer = UpdateContactSerializer(self.contact1, name_data)
        self.assertTrue(serializer.is_valid())
        updated_contact: Contact = serializer.save()
        self.assertEqual(str(updated_contact.name), 'Jenna')

    def test_update_serializer_phone(self) -> None:
        phone_data = self.correct_update_data['only_phone']
        serializer = UpdateContactSerializer(self.contact1, phone_data)
        self.assertTrue(serializer.is_valid())
        updated_contact: Contact = serializer.save()
        self.assertEqual(str(updated_contact.phone), '+12125552368')

    def test_update_serializer_email(self) -> None:
        email_data = self.correct_update_data['only_email']
        serializer = UpdateContactSerializer(self.contact1, email_data)
        self.assertTrue(serializer.is_valid())
        updated_contact: Contact = serializer.save()
        self.assertEqual(str(updated_contact.email), 'new@new.com')

    def test_update_serializer_priority(self) -> None:
        priority_data = self.correct_update_data['only_priority_group']
        serializer = UpdateContactSerializer(self.contact1, priority_data)
        self.assertTrue(serializer.is_valid())
        updated_contact: Contact = serializer.save()
        self.assertEqual(str(updated_contact.priority_group), 'High')

    def test_update_serializer_email_and_phone(self) -> None:
        email_and_phone_data = self.correct_update_data['email_and_phone']
        serializer = UpdateContactSerializer(self.contact1, email_and_phone_data)
        self.assertTrue(serializer.is_valid())
        updated_contact: Contact = serializer.save()
        self.assertEqual(str(updated_contact.email), 'new@new.com')
        self.assertEqual(str(updated_contact.phone), '+12125552368')

    def test_update_serializer_all_fields(self) -> None:
        all_fields = self.correct_update_data['all_fields']
        serializer = UpdateContactSerializer(self.contact1, all_fields)
        self.assertTrue(serializer.is_valid())
        updated_contact: Contact = serializer.save()
        self.assertEqual(str(updated_contact.name), 'Jenna')
        self.assertEqual(str(updated_contact.email), 'new@new.com')
        self.assertEqual(str(updated_contact.phone), '+12125552368')
        self.assertEqual(str(updated_contact.priority_group), 'High')

    def test_update_serializer_empty_name(self) -> None:
        name_data = self.wrong_update_data['empty_name']
        serializer = UpdateContactSerializer(self.contact1, name_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors.keys()), ['name'])

    def test_update_serializer_incorrect_phone(self) -> None:
        phone_data = self.wrong_update_data['incorrect_phone']
        serializer = UpdateContactSerializer(self.contact1, phone_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors.keys()), ['phone'])

    def test_update_serializer_incorrect_email(self) -> None:
        phone_data = self.wrong_update_data['incorrect_email']
        serializer = UpdateContactSerializer(self.contact1, phone_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors.keys()), ['email'])

    def test_update_serializer_no_phone_and_email(self) -> None:
        phone_email_data = self.wrong_update_data['no_phone_and_email']
        serializer = UpdateContactSerializer(self.contact1, phone_email_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors.keys()), ['non_field_errors'])

    def test_update_serializer_no_phone_with_no_email_instance(self) -> None:
        phone_data = self.wrong_update_data['no_phone_with_no_email_instance']
        self.contact1.email = None
        self.contact1.save()
        serializer = UpdateContactSerializer(self.contact1, phone_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors.keys()), ['non_field_errors'])

    def test_update_serializer_no_email_with_no_phone_instance(self) -> None:
        email_data = self.wrong_update_data['no_email_with_no_phone_instance']
        self.contact1.phone = None
        self.contact1.save()
        serializer = UpdateContactSerializer(self.contact1, email_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors.keys()), ['non_field_errors'])
