from django.test import TestCase
from django.conf import settings
from users.models import User
from texts.models import TextBlock


class TestTextBlockModel(TestCase):
    def setUp(self) -> None:
        self.text1 =\
            "Lorem Ipsum is simply dummy text "\
            "of the printing and typesetting industry. "\
            "Lorem Ipsum has been the industry's "\
            "standard dummy text ever since the 1500s, "\
            "when an unknown printer took a galley of "\
            "type and scrambled it to make a type specimen book."
        self.text2 =\
            "Contrary to popular belief, "\
            "Lorem Ipsum is not simply random text."
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.text_block1 = TextBlock.objects.create(
            author=self.user, text=self.text1)
        self.text_block2 = TextBlock.objects.create(text=self.text2)

    def test_creation(self):
        self.assertIsInstance(self.text_block1, TextBlock)
        self.assertIsInstance(self.text_block2, TextBlock)
        block1_repr = str(self.text_block1)
        block2_repr = str(self.text_block2)
        self.assertEqual(block1_repr, f"Text of {self.user.username}")
        self.assertEqual(block2_repr, "Text of unknown user")

    def test_hash_creation(self):
        self.assertIsInstance(self.text_block1.hash, str)
        self.assertEqual(len(self.text_block1.hash),
                         settings.DEFAULT_HASH_LENGTH)
