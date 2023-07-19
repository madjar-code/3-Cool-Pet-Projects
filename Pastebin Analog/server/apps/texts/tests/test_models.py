import pytest
from django.utils import timezone
from users.models import User
from texts.models import TextBlock, Device


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        username='testuser', email='test@test.com', password='testpass')
    return user


@pytest.fixture
def test_text_block(test_user: User):
    text_block = TextBlock.objects.create(
        title='Test Text',
        text='This is a test text.',
        author=test_user,
        expiration_time=timezone.now() + timezone.timedelta(days=1),
    )
    return text_block


def test_create_text_block(test_text_block: TextBlock):
    assert TextBlock.objects.count() == 1
    assert TextBlock.objects.first().title == 'Test Text'


def test_text_block_str(test_text_block: TextBlock):
    text_block = TextBlock.objects.first()
    assert str(text_block) == f'Text of {text_block.author}'


def test_text_block_expiration_time(test_text_block: TextBlock):
    text_block = TextBlock.objects.first()
    assert text_block.expiration_time > timezone.now()


def test_text_block_view_count(test_text_block: TextBlock):
    text_block = TextBlock.objects.first()
    assert text_block.view_count == 0


def test_text_block_viewed_devices(test_text_block: TextBlock):
    device = Device.objects.create(ip_address='192.168.1.1')
    text_block = TextBlock.objects.first()
    text_block.viewed_devices.add(device)
    assert text_block.viewed_devices.count() == 1


def test_text_block_manager(test_text_block: TextBlock):
    assert TextBlock.active_objects.count() == 1
    assert TextBlock.active_objects.count() == 1
