from typing import List, OrderedDict, Any
from django.test import TestCase
from mixer.backend.django import mixer
from users.models import User
from texts.models import TextBlock
from texts.api.serializers import (
    SimpleTextBlockSerializer,
    TextBlockSerializer,
    CUTextBlockSerializer,
)


class TestTextBlockSerializers(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='test', email='test@test.com', password='test')

        self.text_block1: TextBlock = mixer.blend(
            TextBlock, author=self.user, text=mixer.faker.text())
        self.text_block2: TextBlock = mixer.blend(
            TextBlock, author=self.user, text=mixer.faker.text())
        self.text_block3: TextBlock = mixer.blend(
            TextBlock, text=mixer.faker.text())
        self.text_block4: TextBlock = mixer.blend(
            TextBlock, text=mixer.faker.text())

        self.simple_serializer = SimpleTextBlockSerializer(
            instance=[self.text_block1, self.text_block2], many=True)
        self.detail_serializer1 = TextBlockSerializer(
            instance=self.text_block1)
        self.detail_serializer2 = TextBlockSerializer(instance=self.text_block3)

        self.create_serializer1 = CUTextBlockSerializer(
            data={'text': 'Test Text'})
        self.create_serializer2 = CUTextBlockSerializer(
            data={'text': 'Test Text', 'expiration_time': '2023-06-01T07:25:39.447Z'})
        self.create_serializer3 = CUTextBlockSerializer(
            data={'text': 'Test Text', 'author': self.user.id})
        self.create_serializer4 = CUTextBlockSerializer(
            data={'text': 'Test Text', 'expiration_time': 'wrong_time'})
        

    def test_simple_serializer(self):
        serialized_data: List[OrderedDict[str, Any]] = self.simple_serializer.data
        self.assertEqual(len(serialized_data), 2)

        self.assertEqual(list(serialized_data[0].keys()), ['id', 'author', 'hash'])
        self.assertEqual(list(serialized_data[1].keys()), ['id', 'author', 'hash'])

    def test_detail_serializer(self):
        serialized_data: OrderedDict[str, Any] = self.detail_serializer1.data
    
        self.assertEqual(list(serialized_data.keys()),
                         ['id', 'author', 'hash', 'text', 'expiration_time'])

    def test_create_serializer_only_text(self):
        serializer: CUTextBlockSerializer = self.create_serializer1
        self.assertTrue(serializer.is_valid())

    def test_create_serializer_text_exp_time(self):
        serializer: CUTextBlockSerializer = self.create_serializer2
        self.assertTrue(serializer.is_valid())

    def test_create_serializer_text_author(self):
        serializer: CUTextBlockSerializer = self.create_serializer3
        self.assertTrue(serializer.is_valid())

    def test_create_serializer_text_exp_time_wrong_data(self):
        serializer: CUTextBlockSerializer = self.create_serializer4
        self.assertFalse(serializer.is_valid())
        self.assertIn('expiration_time', serializer.errors)
        error_message = serializer.errors['expiration_time'][0]
        self.assertEqual(error_message, 'Invalid date format')
