from enum import Enum
from django.test import TestCase
from django.core.exceptions import ValidationError
from contacts.models import (
    PriorityChoices,
    Contact,
)


class TestContactModel(TestCase):
    def setUp(self) -> None:
        self.contact1: Contact = Contact.objects.create(
            name='test1',
            email='test1@test.com',
            phone='+12125552368',
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

    def test_representation(self) -> None:
        self.assertEqual(str(self.contact1), 'test1')
        self.assertEqual(str(self.contact2), self.contact2.name)

    def test_creation(self) -> None:
        self.assertIsInstance(self.contact1, Contact)
        self.assertIsInstance(self.contact2, Contact)

    def test_priority_group(self) -> None:
        self.assertIsInstance(self.contact1.priority_group, Enum)
        self.assertEqual(str(self.contact1.priority_group), 'Low')

    def test_clean_empty_fields(self) -> None:
        contact = Contact(
            name='test3',
            priority_group=PriorityChoices.BLACKLIST,
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()
