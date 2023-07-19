import pytest
from django.utils import timezone
from typing import Dict, Any
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from users.models import User
from texts.models import TextBlock
from texts.api.serializers import (
    SimpleTextBlockSerializer,
    CUTextBlockSerializer,
)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_user(db) -> User:
    user = User.objects.create_user(
        username='testuser', email='test@test.com', password='testpass')
    return user


@pytest.fixture
def test_text_block(test_user: User) -> TextBlock:
    text_block = TextBlock.objects.create(
        title='Test Text',
        text='This is a test text.',
        author=test_user,
    )
    return text_block


def test_simple_text_block_serializer(api_client: APIClient, test_text_block: TextBlock):
    serializer = SimpleTextBlockSerializer(instance=test_text_block)
    serialized_data: Dict[str, Any] = serializer.data

    assert serialized_data['id'] == str(test_text_block.id)
    assert serialized_data['title'] == test_text_block.title
    assert serialized_data['author'] == test_text_block.author.id
    assert serialized_data['view_count'] == test_text_block.view_count
    assert serialized_data['hash'] == test_text_block.hash


def test_cu_text_block_serializer_create(test_user: User):
    serializer_data: Dict[str, Any] = {
        'title': 'Test Text',
        'text': 'This is a test text.',
        'author': test_user.id,
        'time_delta': 60,
    }

    serializer = CUTextBlockSerializer(data=serializer_data)
    assert serializer.is_valid()

    instance: TextBlock = serializer.save()

    assert instance.title == serializer_data['title']
    assert instance.text == serializer_data['text']
    # assert instance.author == test_user
    assert instance.view_count == 0
    assert instance.expiration_time > timezone.now()


def test_cu_text_block_serializer_create_no_time_delta(test_user: User):
    serializer_data: Dict[str, Any] = {
        'title': 'Test Text',
        'text': 'This is a test text.',
        'author': test_user.id,
    }

    serializer = CUTextBlockSerializer(data=serializer_data)
    assert serializer.is_valid()

    instance: TextBlock = serializer.save()

    assert instance.title == serializer_data['title']
    assert instance.text == serializer_data['text']
    # assert instance.author == test_user
    assert instance.view_count == 0
    assert instance.expiration_time is None


def test_cu_text_block_serializer_create_null_time_delta(test_user: User):
    serializer_data: Dict[str, Any] = {
        'title': 'Test Text',
        'text': 'This is a test text.',
        'author': test_user.id,
        'time_delta': None,
    }

    serializer = CUTextBlockSerializer(data=serializer_data)
    assert serializer.is_valid()

    instance: TextBlock = serializer.save()

    assert instance.title == serializer_data['title']
    assert instance.text == serializer_data['text']
    # assert instance.author == test_user
    assert instance.view_count == 0
    assert instance.expiration_time is None


def test_cu_text_block_serializer_update(test_user: User):
    text_block = TextBlock.objects.create(
        title='Existing Text',
        text='This is an existing text.',
        author=test_user,
    )

    serializer_data: Dict[str, Any] = {
        'title': 'Updated Text',
        'text': 'This is an updated text.',
        'time_delta': 120,
    }

    serializer = CUTextBlockSerializer(instance=text_block, data=serializer_data, partial=True)
    assert serializer.is_valid()

    instance: TextBlock = serializer.save()

    assert instance.title == serializer_data['title']
    assert instance.text == serializer_data['text']
    # assert instance.author == test_user
    assert instance.view_count == text_block.view_count
    assert instance.expiration_time > timezone.now()


def test_cu_text_block_serializer_invalid_time_delta(test_user: User):
    serializer_data: Dict[str, Any] = {
        'title': 'Test Text',
        'text': 'This is a test text.',
        'author': test_user.id,
        'time_delta': 'invalid_time',
    }

    serializer = CUTextBlockSerializer(data=serializer_data)
    assert not serializer.is_valid()
