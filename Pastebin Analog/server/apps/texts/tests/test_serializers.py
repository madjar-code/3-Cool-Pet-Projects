import uuid
from typing import List, OrderedDict, Any
from django.test import TestCase
from mixer.backend.django import mixer
from users.models import User
from texts.models import TextBlock
from texts.api.serializers import (
    SimpleTextBlockSerializer,
    TextBlockSerializer,
)


class TestTextBlockSerializers(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
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

    def test_simple_serializer(self):
        serialized_data: List[OrderedDict[str, Any]] = self.simple_serializer.data
        self.assertEqual(len(serialized_data), 2)

        self.assertEqual(list(serialized_data[0].keys()), ['id', 'author', 'hash'])
        self.assertEqual(list(serialized_data[1].keys()), ['id', 'author', 'hash'])

    def test_detail_serializer(self):
        serialized_data: OrderedDict[str, Any] = self.detail_serializer1.data
    
        self.assertEqual(list(serialized_data.keys()),
                         ['id', 'author', 'hash', 'text'])
